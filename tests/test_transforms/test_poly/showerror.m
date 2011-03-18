
fileList = dir('errorarray*.txt');
fLength = length(fileList);
for i=1:fLength;
    errortext = load(fileList(i).name);
    errorarray = reshape(errortext,[25,75])';
    %errorarray(errorarray <= 0.1) = 0;

    fig = figure;
    set(fig, 'Resize', 'off');
    set(fig, 'Position', [100 100 250 500]);
    [co, co] = contourf(errorarray,100);
    caxis([0,1]);
    colorbar;
    set(co, 'edgecolor','none');
    set(gca, 'PlotBoxAspectRatio', [1,3,1]);
    set(gca, 'YDir', 'reverse');
end;