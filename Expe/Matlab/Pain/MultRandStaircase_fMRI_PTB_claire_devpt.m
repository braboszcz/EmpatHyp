
% Last updated 15:35, 20.11.2013 
%
clear all

c = exptSetup;

    data.font_size = 100;
    data.font = 'Helvetica';
    data.font_color = 225;
    data.background_color = 0;
    

%pathroot = 'D:\LABNIC\Claire\empathyp'; % BBL Folder
pathroot = '/home/claire/Documents/Projet Hypnose/HypnoScript/EmpatHyp/Expe/Matlab/Pain';   
addpath(pathroot);
%
rating_time = 8; % the maximum duration of the rating period
%
% Output file
%
clear OUT*
% Block information
% Check if it's the 1st block, 
% - if it is take all personal details 
% - if not take only name [and complete the other details automatically from a preveious made OUT structure]
%
    OUT.subject = input('Please enter your subject ID number: ','s');;
    OUT.block=input('Enter session (norm or hypno):', 's');
%
% Loading the orientation of the Likert scale per subject
%
%
% MSA settings
%
port = 4;
inifile = '365_Thermod_v5_fmri_v.6_748_130827.ini';

%!!!!! Uncomment for WINDOWS
%addpath([pathroot, '\pain\msa\Matlab']) %scripts for thermal stimulation
addpath([pathroot, '/pain/msa/Matlab'])
%MsaOpen(port,inifile);
%
% PTB settings
%
 %   Find out if there is more than one screen:
%     if max(Screen('Screens')) > 0
%           If so, get the primary screen's resolution
%         dual=get(0,'MonitorPositions');
%         resolution = [0,0,dual(1,3),dual(1,4)];
%         
%     elseif max(Screen('Screens'))==0
%           If not, get the normal screen's resolution
%         resolution = get(0,'ScreenSize') ;
%     end
%     
%     data.screenX = resolution(3);
%     data.screenY = resolution(4);
% 
%     Determine the screen number:
%     screenNumber = max(Screen('Screens'));
%     
%     [Window,Rect] = Screen('OpenWindow',screenNumber,0, [0 0 640 480]);
%     
%     Screen('TextSize',Window,data.font_size);
%     Screen('TextFont',Window,data.font);

    %map = getmousemap;
%
% Other settings
%
clear Trialwise
nTurn = 3; %number of turing points (4)
nStair = 1; % number of multiple random staircases (2)
%
% Setting the critical threshold turning point
%  set it manually
%
Critical2 = [2]; % [-40] Insert Manually in a scale from 0-100 critical threshold turning point
Critical=Critical2(1);

TBase=37; % Baseline temperature
TStartMin = 40; %Starting temperature 
TStartMax = TStartMin+4; % maximum possible baseline temperature
BigChange = 2; %temperature changes for two identical consecutive resp. 
SmallChange = 1; %temperature changes for different consecutive resp.
trial_dur = 2000; %duration (ms)
raise_dur = 3000; % how much time (ms)
slope = 4;
%settextstyle('Verdana Bold Italic',25);
%
% match the language instruction
%

     Kstrings={'+','La température change... ','Seuil estimé: '}; %strings used in the text
% elseif strcmp(lang,'English')
%     Kstrings={'+','The temperature changes... ','Estimated threshold: '}; %strings used in the text
% end
%

Resp = 0;
Revtemp = NaN(nStair,nTurn);
PResp = zeros(1,nStair);
AResp = zeros(1,nStair);
Revcount = zeros(1,nStair);
TStair = zeros(1,nStair);
for i = 1:nStair
    TStair(1,i) = ceil(TStartMin + ((TStartMax - TStartMin)/nStair)*(i-1));
end
%
% Start trials loop
%
t0=GetSecs();
OUT.t0 = t0;
it = 0;
icheck = 0;
%MsaReachStimTemp(TBase,slope)
%ccd_MsaMonitor(TBase)
while icheck == 0;
    it = it+1;
    %
    % precaution
    %
    if it > 80
        break
    end
    
    %
    % random selection of staircase
    %
    clear rsel is isv
    isv = find(Revcount < nTurn);
    rsel = ceil(rand*length(isv)); %randomly select an integer from 1 to nStair
    is = isv(rsel);
    %
    % Clear display buffer 1
    %
  %  clearpict( 1 );
    %
    % fixation
    %
   % clearpict( 1 )
    DrawFormattedText(c.Window,Kstrings{1},'center','center',225);
  
    Screen('Flip',c.Window);
    WaitSecs(1);
    %
    % stimulation
    %
    slope = ceil((TStair(is) - TBase)/(raise_dur/1000));
    if slope > 5
        slope = 5;
    end
    if slope < 1
        slope = 1;
    end
    tss = GetSecs();
    %MsaReachStimTemp(TStair(is),slope)
    
   %DrawFormattedText(c.Window,Kstrings{2},'center','center',225);
    %Screen('Flip',c.Window);
    %ccd_MsaMonitor(TStair(is))
    tsr = GetSecs();
   % WaitSecs( trial_dur+(raise_dur-(tsr-tss)) );
    %MsaReachStimTemp(TBase,slope)
    %
    % clear screen
    %
%     clearpict( 1 )
%     drawpict( 1 );
    %WaitSecs(0.5); 
    %
    
    %% NEW-VERSION RATING with Likert-Scale
    %
    [rating, RT]=circleLikert_claire(c, rating_time); % rating time + max duration of rating period
    Resp=rating;     
    %
   
    if Resp >= Critical
        AResp(is) = 0;
    else
        AResp(is) = 1;
    end
    
    %
% Screen output
%
TRIAL=it
STAIRCASE=is
TEMPERATURE=TStair(is)
RATING=Resp

    %
    % set output
    %
    Trialwise(it,1) = it; %column 1: trial
    Trialwise(it,2) = is; %column 2: staircase
    Trialwise(it,3) = TStair(is); %column 3: temperature used
    Trialwise(it,4) = tss - t0; %column 4: time stimulation starts
    Trialwise(it,5) = tsr - t0; %column 5: time stimulation reaches point
    Trialwise(it,6) = Resp; %column 6: temperature rating
    Trialwise(it,7) = RT; %column 7: Response Time
    %
    % what happens if the Critical value has not been crossed?
    %
    if AResp(is) == PResp(is)
        if AResp(is) == 0
            TStair(is) = TStair(is) + BigChange;
        else
            TStair(is) = TStair(is) - BigChange;
        end
    else
        %
        % what happens if the Critical value has been crossed?
        %
        Revcount(is) = Revcount(is) + 1;
        Revtemp(is,Revcount(is)) = TStair(is);
        if AResp(is) == 1
            TStair(is) = TStair(is) - SmallChange;
        else
            TStair(is) = TStair(is) + SmallChange;
        end
    end
    %
    % precaution
    %
    if TStair(is) > 52;
        TStair(is) = 52;
    end
    %
    PResp(is) = AResp(is);    
    %
    % Clear screen
    %
    DrawFormattedText(c.Window,Kstrings{1},'center','center',225);
    Screen('Flip', c.Window)
    %
    % wait until temperature gets to baseline
    %
    WaitSecs(1);
    %ccd_MsaMonitor(TBase)
    % 
    clear isv
    isv = find(Revcount < nTurn);
    if numel(isv) == 0
        icheck = 1;
    end
end
%MsaClose
%
% Online threshold calculation
%
Thr = nanmean(reshape(Revtemp,1,nStair*nTurn));
%settextstyle('Verdana Bold Italic',25);
DrawFormattedText(c.Window,[Kstrings{3}, num2str(Thr),' �C' ],'center','center',data.font_color);
Screen('Flip', c.Window)
KbWait();
t1=time;
OUT.t1 = t1 - t0;
sca;
%
% Saving the subject's data
%
OUT.Trialwise = Trialwise;
OUT.Thr = Thr;
OUT.Revtemp = Revtemp;
filename_current = ['Pain_',OUT.subject]; % current data [for threshold extraction]
filename_track = ['Pain_',OUT.subject,'_',num2str(OUT.block)]; % backup data 
eval(['save ',filename_current,' OUT -V6']);
eval(['save ',filename_track,' OUT -V6']);
%
% Plot figure results
%
figure(1)
subplot(2,2,1)
hold on
for i = 1:nStair
    plot(Trialwise(Trialwise(:,2)==i,1),Trialwise(Trialwise(:,2)==i,3),'k-x')
end
line([1,Trialwise(size(Trialwise,1))],[Thr Thr])
axis([1,size(Trialwise,1),36,55])
