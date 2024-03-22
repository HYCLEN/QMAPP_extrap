function [q_Base_CDF, Base_CDF]=Cunnane_CDF(Base_CDF)

% Unbiased quantile estimator (Cunnane formulation)
Rank_Base_CDF=[1:length(Base_CDF)]';
Base_CDF=sort(Base_CDF,'descend');
q_Base_CDF=(Rank_Base_CDF-0.4)./(length(Base_CDF)+0.2);


% % plots
% figure
% plot(q_Target_CDF, Target_CDF, 'b')
% hold on
% plot(q_Base_CDF, Base_CDF,'k--')
% legend('Target CDF', 'Base CDF' ,'FontSize' , '12')
% 
% figure
% plot(q_DATA, Sorted_DATA,'r')
% hold on
% plot(q_Output, Sorted_Output,'g--')
% legend('Input Data','Output Data','FontSize' , '12')
% 
% figure
% plot(q_Target_CDF, Target_CDF,'b')
% hold on
% plot(q_Output, Sorted_Output,'g--')
% legend('Target CDF','Output Data','FontSize' , '12')

% figure
% plot(q_Output_ori, Sorted_Output_ori,'b')
% hold on
% plot(q_Output_normal, Sorted_Output_normal,'g--')
% hold on
% plot(q_Output_delta, Sorted_Output_delta,'r--')
% hold on
% legend('Output original', 'Output normal','Output delta','FontSize' , '12')

end

