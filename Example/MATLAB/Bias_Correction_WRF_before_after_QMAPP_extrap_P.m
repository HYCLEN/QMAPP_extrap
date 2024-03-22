%% Example implementation of quantile mapping to correct bias of outliers falling outside of base CDF
% Sample data: daily total precipitation of July for the reference period (1995-2004) and target period (2085-2094)
%             (1) 'OBS_1995-2004': observed data
%             (2) 'HR_1995-2004': historical run of Regional Climate Model(RCM)   
%             (3) 'CCR_2085-2094': future climate change run of RCM

%% Work space & Import data

cd=pwd;

T = readtable("P_sample.csv",'VariableNamingRule','preserve');
P_OBS = table2array(T(:,1)); % observed data(1995-2004)
P_HR = table2array(T(:,2));  % historical run(1995-2004)
P_CCR = table2array(T(:,3)); % climate change run(2085-2094)

%% Main process: Bias correction using qunatile mapping
    
% Bias correction for CCR
P_CCR_BC = QMAPP_extrap(P_OBS, P_HR, P_CCR, 0);

%% Plot results

% creating plotting position using Cunnane unbiased quantile estimator
[x_or y_or]=Cunnane_CDF(P_OBS); % observed for reference period
[x_mr y_mr]=Cunnane_CDF( P_HR); % model for reference period
[x_bef y_bef]=Cunnane_CDF(P_CCR); % model for future (before bias correction)
[x_af y_af]=Cunnane_CDF(P_CCR_BC); % model for future (after bias correction)


%Figure configuration
figure(1) % Problem in conventional methods

%figure size
allfig = findobj('Type','figure');
set(allfig , 'Units', 'centimeters')
set(allfig, 'PaperUnits', 'centimeters')
xwidth=17;
ywidth=18;
set(allfig , 'Position', [5 5 xwidth ywidth])
set(allfig, 'PaperSize',  [xwidth ywidth])
set(allfig, 'PaperPositionMode', 'auto')


% flag values falling outside of the range of historical CDF
idx_out = find(y_bef>max(y_mr));

h1= subplot(2,1,1);
axes(h1) % before correction
size=6;
p1=plot(x_or, y_or, 'k-o', 'MarkerSize',size);
hold on
p2=plot(x_mr, y_mr, 'b-s', 'MarkerSize',size);
hold on
p3=plot(x_bef(idx_out(end):end), y_bef(idx_out(end):end),'g-d', 'MarkerEdgeColor','k', 'MarkerFaceColor','g', 'MarkerSize',size);
hold on
p4=plot(x_bef(idx_out), y_bef(idx_out),'r-d', 'MarkerEdgeColor','k', 'MarkerFaceColor','r', 'MarkerSize',size);
hold on

set(gca,'FontSize', 13)
xlabel('Probability of Exceedance', 'FontWeight', 'bold')
ylabel('Daily Total Precipitation (mm)', 'FontWeight', 'bold')
set(gca,'XLim',[0 0.025]);
set(gca,'XTickLabelMode','auto');
set(gca,'YTickLabelMode','auto');
set(gca,'box', 'on')

% legend
leg1=legend([p1 p2 p3 p4],'Observed', 'Historical Simulation', ['Raw Future Simulation'], ['Raw Future Simulation' newline 'Needing Extrapolation'], 'Location','Northeast');
leg1.FontSize = 13;
leg1.FontWeight = 'bold';
leg1.Box = 'off';
leg1.EdgeColor='none';

h2= subplot(2,1,2); 
axes(h2) %after correction
size=6;
p1=plot(x_or, y_or, 'k-o', 'MarkerSize',size);
hold on
p2=plot(x_mr, y_mr, 'b-s', 'MarkerSize',size);
hold on
p3=plot(x_af, y_af,'r-*', 'MarkerEdgeColor','r', 'MarkerFaceColor','r', 'MarkerSize',size);
hold on

set(gca,'FontSize', 13)
xlabel('Probability of Exceedance', 'FontWeight', 'bold')
ylabel('Daily Total Precipitation (mm)', 'FontWeight', 'bold')
set(gca,'XLim',[0 0.025]);
set(gca,'XTickLabelMode','auto');
set(gca,'YTickLabelMode','auto');
set(gca,'box', 'on')

% legend
leg1=legend([p1 p2 p3],'Observed', 'Historical Simulation', ['Bias-Corrected' newline 'Future Simulation'], 'Location','Northeast');
leg1.FontSize = 13;
leg1.FontWeight = 'bold';
leg1.Box = 'off';
leg1.EdgeColor='none';

            
