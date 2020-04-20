function [Duration, Frequency, Intensity, Severity, Recovery] = Fx_PteropodThresholds_v02( ...
    ThresholdMagnitude, ThresholdDuration, InputData, outPerDay)

% Matlab function to calculate metrics for model output of pteropod thresholds
% for input of a two-dimensional array of aragonite saturation state omega
% InputData array has dimensions of nodes x times
% Output vectors of trheshold metrics have length of number of nodes
%
% Written by:
%
% Greg Pelletier 
% Washigton State Department of Ecology
% Olympia WA
% greg.pelletier@ecy.wa.gov
% 
% INPUTS
%
% - ThresholdMagnitude is the threshold value of Omega-aragonite 
%
% - ThresholdDuration is the minimum event duration (days) to define an adverse event below
% the ThresholdMagnitude
%
% - InputData is a two-dimensional array (nodes, times) with the time series
% of omega values for each model node
%
% - outPerDay is the time interval (day^-1) for the time series of InputData
% (e.g. 24= hourly model outputs, 4= model outputs every 6 hours, etc.)
%
% OUTPUTS (vectors with length equal to number of model nodes)
% 
% - Duration is the cumulative duration (days) of events below the
% ThresholdMagnitude for events longer than ThresholdDuration for each model node
% 
% - Frequency is the cumulative frequency (number of events) of events below the
% ThresholdMagnitude for events longer than ThresholdDuration for each model node
% 
% - Intensity is the mean value of Omega-aragonite of events below the
% ThresholdMagnitude for events longer than the ThresholdDuration for each model node
% (Hauri et al 2013 eqn 1)
%
% - Severity is the product of Intensity and Duration for each model node 
% (Hauri et al eqn 2)
%
% - Recovery is the average recovery period (days) between adverse events

clear Duration Frequency Intensity Severity Recovery ndays;
Duration = zeros(1,numel(InputData(:,1)));   % number of nodes = numel(InputData(:,1)
Frequency = zeros(1,numel(InputData(:,1)));
Intensity = zeros(1,numel(InputData(:,1)));
Severity = zeros(1,numel(InputData(:,1)));
Recovery = zeros(1,numel(InputData(:,1)));
ndays=numel(InputData(1,:))/outPerDay;   % total number of days being evaluated

for inode=1:numel(InputData(:,1))          % loop through nodes
  eventCounter=0; 
  durationCounter=0;
  eventInProgress=0;
  sumIntensity=0;
  nIntensity=0;
  sumIntensityThisEvent=0;
  nIntensityThisEvent=0;
  for itime=1:numel(InputData(1,:))
    % loop through times
    if InputData(inode, itime)<=ThresholdMagnitude
      durationCounter = durationCounter + (1/outPerDay);    
      eventInProgress=1;
      sumIntensityThisEvent = sumIntensityThisEvent + ThresholdMagnitude - InputData(inode, itime); 
      nIntensityThisEvent = nIntensityThisEvent + 1;
    elseif InputData(inode, itime)>ThresholdMagnitude 
      if eventInProgress == 1 && durationCounter >= ThresholdDuration
        eventCounter = eventCounter + 1;
        % accumulate the metrics of this event that occured before the last
        % time in the time series
        Duration(inode)=Duration(inode) + durationCounter;    % cumulative days of events below threshold
        sumIntensity = sumIntensity + sumIntensityThisEvent;
        nIntensity = nIntensity + nIntensityThisEvent;
      end
      % reset counters for next event in this time series
      durationCounter = 0;
      eventInProgress = 0;
      sumIntensityThisEvent = 0;
      nIntensityThisEvent = 0;
    end
    if itime == numel(InputData(inode,:))
      if eventInProgress == 1 && durationCounter >= ThresholdDuration
        eventCounter = eventCounter + 1;
        % accumulate the metrics of this event that was ongoing on the last time
        % in the time series
        Duration(inode) = Duration(inode) + durationCounter;    % cumulative days of events below threshold
        sumIntensity = sumIntensity + sumIntensityThisEvent;
        nIntensity = nIntensity + nIntensityThisEvent;
      end
    end    
    % update the number of events counted in this time series for this node
    Frequency(inode)=eventCounter;
  end  % loop through times
  % save the metrics integrated for the time series for this node
  if nIntensity > 0 
    Intensity(inode) = sumIntensity ./ nIntensity;    % difference between threshold and average omega of events (omega units)
    Severity(inode) = Intensity(inode) .* Duration(inode); % average Omega-days of events below omega threshold
    Recovery(inode) = (ndays - Duration(inode)) ./ Frequency(inode); % average recovery time of favorable condtions between events below threshold
  end
end  % loop through nodes

end