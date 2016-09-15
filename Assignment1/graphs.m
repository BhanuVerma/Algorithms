x = [64,128,259,530,1054,2183,4411,9875,29779,106361,372670,1770677];
y = [0.227,0.494,1.188,2.719,4.411,9.212,21.301,43.987,126.775,391.355,1051.570,4669.690];
figure
plot(x,y)
title('Plot 1 - Static Computation');
xlabel('number of edges'); % x-axis label
ylabel('time for static computation (ms)'); % y-axis label
% legend('y = computation time','x = no. of edges'); 