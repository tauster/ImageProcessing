%%%%%%%%%%%%%%%%%%%%
%   Trajectory
%   Finder
%   
%	Tausif S., 2017
%	
%   Run one section
%   at a time.
%%%%%%%%%%%%%%%%%%%%

clear all
close all

%% Loading scanned map data.
trueTraj = csvread('2017-04-24_10-01-35_XYposition_log_ProjectDemo.csv');
traj = csvread('traj_points.csv', 2, 0);
traj(:, 1) = [];

%% K-means clustering for waypoints.
% Applying k-means clustering function to find "average" waypoints.
k = 50; % Clusters.
[index, waypoints_pre] = kmeans(traj, 50);

% Scatter plot of new points to help with sorting.
figure(1)
%scatter(traj(:, 1), traj(:, 2))
hold on
% Plotting in segments with different markers for easier readibility.
scatter(waypoints_pre(1:10, 1), waypoints_pre(1:10, 2), 'o')
scatter(waypoints_pre(11:20, 1), waypoints_pre(11:20, 2), '*')
scatter(waypoints_pre(21:30, 1), waypoints_pre(21:30, 2), 'x')
scatter(waypoints_pre(31:40, 1), waypoints_pre(31:40, 2), 's')
scatter(waypoints_pre(41:50, 1), waypoints_pre(41:50, 2), '^')
scatter(traj(:, 1), traj(:, 2), 'V')
legend('Set 1:10', 'Set 11:20', 'Set 21:30', 'Set 31:40', 'Set 41:50')
grid on
grid minor
hold off

% Store readjusted waypoints here, use next section to verify lap.
waypoints = waypoints_pre;

%% Readjusted order of trajectory points for lap.
figure(2)
plot(waypoints(:, 1), waypoints(:, 2), '-x')
hold on
scatter(waypoints_pre(:, 1), waypoints_pre(:, 2))
legend('Sorted Trajectory', 'K-Means Clusters')
% plot(trueTraj(:, 1), trueTraj(:, 2), '--')
grid on
grid minor
hold off

%% Finding yaw at each point.
for i = 1:(size(waypoints, 1) - 1)
    vector = waypoints(i + 1, :) - waypoints(i, :);
    
    yaw_pre = atan2(vector(2), vector(1));
    
    if yaw_pre >= 0
        yaw(i, 1) = yaw_pre;
    else
        yaw(i, 1) = yaw_pre + (2*pi);
    end
end

yaw(i + 1) = yaw(i);
yaw = floor(yaw*(180/pi));

%% Final concatination of trajectory points for desired_positions.py
race_trajectory = [round(waypoints, 2), yaw];

csvwrite('race_trajectory.csv', race_trajectory)
