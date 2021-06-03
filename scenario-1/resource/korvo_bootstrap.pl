#!perl
#
#  Run this perl script in an empty directory
#  Optional arguments are :
#    perl korvo_bootstrap.pl [version-to-install] [install_directory]
#       you can specify version_to_install without specifying install_directory.
#	Default values are version = "stable" and install_dir = "$HOME"
#
use strict;
use warnings;
use Cwd;
use File::Basename;
use File::Spec;
use 5.010;

my $interactive = 0;
my $VERSION_TAG = "stable";
my $INSTALL_DIR = '\$HOME';
my $ARCH = "";
our %korvo_tag;

if (defined $ARGV[0]) {
  if ($ARGV[0] eq "-i") {
    $interactive = 1;
    $VERSION_TAG = "stable";
    shift;
  } elsif ($ARGV[0] eq "-h") {
    print ("Usage:\tkorvo_bootstrap.pl [-i] [version tag] [install dir]\n\n");
    exit;
  } else {
    $VERSION_TAG = $ARGV[0];
  }
} else {
  $VERSION_TAG = "stable";
}
if (defined $ARGV[1]) {
  $INSTALL_DIR = $ARGV[1];
} else {
  $INSTALL_DIR = '\$HOME';
}


update_file("./korvo_build.pl", 0);
update_file("./korvo_tag_db", 0);
update_file("./korvo_arch", 0);

#add execute permissions to korvo_arch
my @fstats = stat("./korvo_arch");
my $fperms = sprintf('%04o', ($fstats[2] & 07777) | 00555 );
chmod oct($fperms), "./korvo_arch";

if ("$ARCH" eq "") {
  $ARCH=`./korvo_arch`;
  chop($ARCH);
}

update_file("./build_config.$ARCH", 1);
update_file("./build_config", 1);
my $TAG_DB = "./korvo_tag_db";
unless (my $return = do $TAG_DB) {
    warn "couldn't parse $TAG_DB: $@" if $@;
    warn "couldn't do $TAG_DB: $!"    unless defined $return;
    warn "couldn't run $TAG_DB"       unless $return;
}

if ($interactive == 1) {
    do {
	print "Specify version tag to use [$VERSION_TAG] : ";
	my $input = <>; chomp $input;
	$VERSION_TAG = $input unless $input eq "";
	print "Specify install directory [$INSTALL_DIR] : ";
	$input = <>; chomp $input;
	$INSTALL_DIR = $input unless $input eq "";
	unless (defined $korvo_tag{"$VERSION_TAG"}) { 
	    print "Couldn't find version \"$VERSION_TAG\" in korvo_tag_db\n";
	    print "Please use a valid tag.  Known tags are:\n";
	    foreach my $tag (keys %korvo_tag) {
	        print "\t$tag\n";
	    }
	    $VERSION_TAG="stable";
	}
    } until (defined $korvo_tag{"$VERSION_TAG"});
}

unless (defined $korvo_tag{"$VERSION_TAG"}) { 
  print "Couldn't find version \"$VERSION_TAG\" in korvo_tag_db\n";
  print "Please use a valid tag.  Known tags are:\n";
  foreach my $tag (keys %korvo_tag)
    {
      print "\t$tag\n";
    }
  die "\n";
}


print "Configuring system for release \"$VERSION_TAG\", install directory \"$INSTALL_DIR\"\n";
if (-f "./build_config.$ARCH") {
  substitute_values("./build_config.$ARCH", $VERSION_TAG, $INSTALL_DIR);
  rename("build_config.$ARCH", "korvo_build_config.$ARCH");
}
substitute_values("./build_config", $VERSION_TAG, $INSTALL_DIR);
rename("build_config", "korvo_build_config");


use Cwd;


sub substitute_values {
    my ($filename, $version, $install_dir) = @_;
    $version = quotemeta $version;
    if (substr($install_dir, 0, 1) eq ".") {
      $install_dir = File::Spec->rel2abs( $install_dir );
    }
    $install_dir = quotemeta $install_dir;
    my $currWorkDir = &Cwd::cwd();
    my $build_dir = quotemeta "$currWorkDir/build_area";
    my $results_dir = quotemeta "$currWorkDir/build_results";
    my $command = "perl -pi -e \'s/VERSION_TAG=.*/VERSION_TAG=$version/\' $filename";
    system($command);
    $command = "perl -pi -e \'s/INSTALL_DIRECTORY=.*/INSTALL_DIRECTORY=$install_dir/\' $filename";
    system($command);
    $command = "perl -pi -e \'s/BUILD_AREA=.*/BUILD_AREA=$build_dir/\' $filename";
    system($command);
    $command = "perl -pi -e \'s/.*RESULTS_FILES_DIR=.*/RESULTS_FILES_DIR=$results_dir/\' $filename";
    system($command);
}

sub update_file {
    my ($filename, $suppress_errors) = @_;
    my $base = basename $filename;
    my $dir = dirname $filename;
    my ($ua, $response);
    state $has_lwp = -1;

    if (-d $dir . "/.svn") {
      # if under svn, do an svn update 
      system('cd "$dir" ; svn -q update');
      return;
    }
    if ($has_lwp == -1) {
      $has_lwp = eval
	{
	  require LWP::UserAgent;
	  require LWP::Protocol::https;
	  LWP::UserAgent->new();
	  1;
	};
    }
    $has_lwp = 0 unless defined($has_lwp);
    if($has_lwp) {
      # LWP::UserAgent loaded and imported successfully
      my $ua = LWP::UserAgent->new();
      $ua->env_proxy();     
      $response = $ua->get("https://GTkorvo.github.io/$base");
     
      if ($response->is_success) {
	open(FILE, ">/tmp/$base");
	print FILE $response->decoded_content;
	close FILE;
      } else {
        if (! $suppress_errors ) { print "Error updating $base: " . $response->status_line . "\n"; }
	return;
      }
    } else {
      my $ret = system("cd /tmp ; rm -f $base ; wget -q https://GTkorvo.github.io/$base");
      my $exit_value = $ret >> 8;
      if ($exit_value != 0) {
	  if (!$suppress_errors) {
	      die("This script requires either the perl module LWP::UserAgent, or the command 'wget' to be installed\n\tThe former was not found and the latter failed.");
	  }
	  return;
      }
    }

  if (system("cmp -s $filename /tmp/$base") != 0) {
    system("mv /tmp/$base $filename");
    print "Installed fresh $filename\n";
  } else {
    unlink("/tmp/$base");
    print "No need to update $filename\n";
  }
}

