%% Header
% Title: ULN_serial.m
% Created Date: 2025-09-20
% Last modified date: 2026-03-23
% Matlab Version: R2024b
%% Notes:
%
% Example for the ULN lasers using serial commands. Sets TEC mode to auto
% and briefly turns laser on.

%% Configuration
PORT = 'COM3';       % change to your port as shown on device manager
BAUD = 115200;
TIMEOUT = 5;

%% Open serial port
s = serialport(PORT, BAUD);
s.DataBits = 8;
s.Parity = 'none';
s.StopBits = 1;
s.Timeout = TIMEOUT;
configureTerminator(s, 'CR/LF');

%% Send commands
sendCmd(s, 'nop');
pause(0.5);

sendCmd(s, 'laser_tec_ctrl_mode auto');
pause(0.5);

sendCmd(s, 'laser on');
pause(3);

sendCmd(s, 'laser off');
pause(0.5);

clear s;
disp('Done - port closed.');


%% Send command function
function sendCmd(s, cmd)
    writeline(s, cmd);          

    raw = readline(s);          

    % Parse return code E.G 000: OK:response, etc.
    parts = strsplit(raw, ':', 'CollapseDelimiters', false);
    code  = strtrim(parts{1});
    text  = strjoin(parts(2:end), ':'); 

    if strcmp(code, '000')
        fprintf('[OK] %-20s - %s\n', cmd, text);
    else
        fprintf('[ERR] %-20s - %s: %s\n', cmd, code, text);
    end
end