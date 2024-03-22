function [Output]=QMAPP_extrap(Target_CDF, Base_CDF, DATA, min_bound)
%--------------------------------------------------------------------------
% The function allows biascorrection of the input data (DATA) by matching its Baseline Cumulative Distribution Function (Base_CDF) to that of benchmark data (Target_CDF).
%  In particular this version enhances: 
%      (1) Extrapolation of values falling outside of baseline CDF in the way that the change in the first moment is preserved. 
%      (2) Selection of quantile of the same values (e.g. zero precipitation) in the way that ratio of quantile between baseline and target CDF is preserved. 
%                                       
% Input:
%       Target_CDF : Empirical CDF of benchmark data ex) OBS 1950-2000
%       Base_CDF : Empirical CDF of baseline CDF of data to be corrected ex) Monthly GCM for given historical periods 1950-2000
%       DATA : Data to be bias-corrected ex) GCM 1950-2100 including future periods
%       min_bound : if corrected final output should be greater than or equal to a specific value (0 in case of precipitation), user can specify the minimum bound as a numeric value. Otherwise, leave it as 'none'.
%       
%                     
%
% Output:
%       Output : Corrected data by Quantile Mapping
%       n: number of extreme values falling out the range of Base CDF
%
%--------------------------------------------------------------------------

% Make Output vector having the same length with DATA
Output=zeros(size(DATA));

% Unbiased quantile estimator (Cunnane formulation)
Rank_Target_CDF=[1:length(Target_CDF)]';
Rank_Base_CDF=[1:length(Base_CDF)]';

Target_CDF=sort(Target_CDF,'descend');
Base_CDF=sort(Base_CDF,'descend');

q_Target_CDF=(Rank_Target_CDF-0.4)./(length(Target_CDF)+0.2);
q_Base_CDF=(Rank_Base_CDF-0.4)./(length(Base_CDF)+0.2);

% flag1: number of values falling outside of Base_CDF in original DATA
idx1=find(DATA > max(Base_CDF) | DATA < min(Base_CDF) );
n1=length(idx1);

% Determine if any value is below zero, which needs the offset of data
if (min(Target_CDF) < 0 ||  min(Base_CDF) < 0 || min(DATA) < 0)

   min_val = min(min(Target_CDF), min(min(Base_CDF), min(DATA)));
   offset = abs(floor(min_val));
   
   Target_CDF = Target_CDF + offset;
   Base_CDF = Base_CDF + offset;
   DATA = DATA + offset;

end
    

% Quantile mapping
for i = 1:length(DATA)
        
    % if same values exist on the Base_CDF
    if (length(find(Base_CDF == DATA(i))) > 1) 
       apple = find(Base_CDF == DATA(i));
       start_q = q_Base_CDF(apple(1));
       end_q = q_Base_CDF(apple(end));
       length_zero = end_q - start_q;
       scaled_distance = rand;
       q = start_q + (length_zero*scaled_distance);
       [c,  apple]=min(abs(q_Target_CDF - q));
       Output(i) = Target_CDF(apple);
        
        continue;
    end
    
     %% Extrapolation of extreme value 
    % Higher than maximum value of Base CDF 
    if ( DATA(i) > max(Base_CDF) ) 
        
        % Mean of Base CDF
        mu1 = mean(Base_CDF(1:end));
        
        % Calculate mean if the highest value of Base CDF is replaced with the extreme value
        mu2 = (DATA(i)+sum(Base_CDF(2:end)))/length(Base_CDF(1:end));
        
        % Relative changes in the means
        R = (mu2-mu1)/abs(mu1);
        
        % Mean of Target CDF
        mu3 = mean(Target_CDF(1:end));
        
        % Adjust values in a way that preserves the changes in the 1st moment
        Output(i)=(mu3+abs(mu3)*R)*length(Target_CDF(1:end))-sum(Target_CDF(2:end));
               
    % Lower than minimum value of Base CDF 
    elseif ( DATA(i)< min(Base_CDF) ) 
        
        % Mean of Base CDF
        mu1 = mean(Base_CDF(1:end));
        
        % Calculate mean if lowest value is replaced with extreme value
        mu2 = (DATA(i)+sum(Base_CDF(1:end-1)))/length(Base_CDF(1:end));
        
        % Relative changes in the means
        R = (mu2-mu1)/abs(mu1);
        
        % Mean of Target CDF
        mu3 = mean(Target_CDF(1:end));
        
        % Adjust values in a way that preserves the changes in the 1st moment
        Output(i) = (mu3+abs(mu3)*R)*length(Target_CDF(1:end))-sum(Target_CDF(1:end-1));
        
    else
        
        [c , apple]=min(abs(Base_CDF-DATA(i)));
        q=q_Base_CDF(apple);
        [c , apple]=min(abs(q_Target_CDF-q));
        Output(i)=Target_CDF(apple);
    
    end
        
end

% Bring back the data to the original range by substracting offset value.
if (min(Target_CDF) < 0 ||  min(Base_CDF) < 0 || min(DATA) < 0)
    
    Target_CDF = Target_CDF-offset;
    Base_CDF = Base_CDF-offset;
    DATA = DATA-offset;
    Output = Output-offset;
    
end

% if minimum bound is provided, then replace the value outise the bound
if isnumeric(min_bound) 
    
    idx = find(DATA < min_bound);
    DATA(idx) = min_bound ;
   
end


end

