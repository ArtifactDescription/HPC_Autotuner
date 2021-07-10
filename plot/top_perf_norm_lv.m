clear;

subplot(1, 2, 1);

filename = 'lv_exec_time/top_perf_';
for i = 0 : 1 : 1
    smpl_num = (2 ^ i) * 50;
    data = load(strcat(strcat(filename, int2str(smpl_num)), '.csv'));
    if i == 0
        RS = [data(1)];
        AL = [data(2)];
        CEAL = [data(3)];
        CEALH = [data(4)];
        ALpH = [data(5)];
        GEIST = [data(6)];
    else
        RS = [RS; data(1)];
        AL = [AL; data(2)];
        CEAL = [CEAL; data(3)];
        CEALH = [CEALH; data(4)];
        ALpH = [ALpH; data(5)];
        GEIST = [GEIST; data(6)];
    end
end

%expert = ;
best = 24.62;
AVE = [RS, GEIST, AL, CEAL];
AVE = AVE ./ (best * ones(2, 4))
STD = AVE * 0;

h = bar(AVE);
set(h, 'BarWidth', 0.9);    % The bars will now touch each other
hold on;

num_groups = size(AVE, 1);
num_bars = size(AVE, 2);
group_width = min(0.8, num_bars / (num_bars + 1.5));
for i = 1 : num_bars
    x = (1 : num_groups) - group_width / 2 + (2 * i - 1) * group_width / (2 * num_bars);    % Aligning error bar with individual bar
    b = errorbar(x, AVE(:, i), STD(:, i), 'dk');
    set(b, "marker", ".");
    set(b, "markersize", 1);
end
plot([0, num_groups + 1], [1, 1], '--k', 'MarkerSize', 1, 'LineWidth', 2);
hold on;
ax = gca;
ax.YGrid = 'on';
ax.GridLineStyle = '-';

xlabel('Number of Training Samples', 'FontSize', 22);
ylabel('Normalized Execution Time', 'FontSize', 22);
l = legend('RS', 'GEIST', 'AL', 'CEAL', 'Location', 'Northeast', 'Orientation', 'Horizontal');
l.NumColumns = 2;
set(l, 'FontSize', 22);
axis([0.5  num_groups + 0.5  0.99 2]);
set(gca, 'XTicklabel', {'50', '100'});
set(gca, 'YTick', 1 : 0.1 : 2);
set(gca, 'YScale', 'log');
set(gca, 'FontSize', 22);

subplot(1, 2, 2);

filename = 'lv_comp_time/top_perf_';
for i = 0 : 1 : 1
    smpl_num = (2 ^ i) * 25;
    data = load(strcat(strcat(filename, int2str(smpl_num)), '.csv'));
    if i == 0
        RS = [data(1)];
        AL = [data(2)];
        CEAL = [data(3)];
        CEALH = [data(4)];
        ALpH = [data(5)];
        GEIST = [data(6)];
    else
        RS = [RS; data(1)];
        AL = [AL; data(2)];
        CEAL = [CEAL; data(3)];
        CEALH = [CEALH; data(4)];
        ALpH = [ALpH; data(5)];
        GEIST = [GEIST; data(6)];
    end
end

%expert = ;
best = 3.1284;
AVE = [RS, GEIST, AL, CEAL];
AVE = AVE ./ (best * ones(2, 4))
STD = AVE * 0;

h = bar(AVE);
set(h, 'BarWidth', 0.9);    % The bars will now touch each other
hold on;

num_groups = size(AVE, 1);
num_bars = size(AVE, 2);
group_width = min(0.8, num_bars / (num_bars + 1.5));
for i = 1 : num_bars
    x = (1 : num_groups) - group_width / 2 + (2 * i - 1) * group_width / (2 * num_bars);    % Aligning error bar with individual bar
    b = errorbar(x, AVE(:, i), STD(:, i), 'dk');
    set(b, "marker", ".");
    set(b, "markersize", 1);
end
plot([0, num_groups + 1], [1, 1], '--k', 'MarkerSize', 1, 'LineWidth', 2);
hold on;
ax = gca;
ax.YGrid = 'on';
ax.GridLineStyle = '-';

xlabel('Number of Training Samples', 'FontSize', 22);
ylabel('Normalized Computer Time', 'FontSize', 22);
l = legend('RS', 'GEIST', 'AL', 'CEAL', 'Location', 'Northeast', 'Orientation', 'Horizontal');
l.NumColumns = 2;
set(l, 'FontSize', 22);
axis([0.5  num_groups + 0.5  0.99 2]);
set(gca, 'XTicklabel', {'25', '50'});
set(gca, 'YTick', 1 : 0.1 : 2);
set(gca, 'YScale', 'log');
set(gca, 'FontSize', 22);

text(0.62, 2.03, '2.09', 'Color','k','FontSize', 16);

set(gcf, 'position', [100, 100, 1200, 500]);

print('top_perf_norm_lv.eps', '-depsc')
print('top_perf_norm_lv.png', '-dpng')
