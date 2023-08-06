import plot as plot
from color import *

x = list(range(2010,2020))
y = [1,1.1,1.24,1.18,1.5,1.46,1.99,2.0,2.34,2.55]
mat = [1.000,1.024,1.032,1.054,1.045,1.046,1.056,1.035,1.076,1.053]
def translate(alist,mult,add):
    newlist = []
    for elem in alist:
        val = elem*mult+add
        newlist.append(val)
    return newlist

yhigh = translate(y,1.23,0.1)
ylow = translate(y,0.89,-0.1)
pave = plot.line(x,y,legend = 'Average',color = BLUE)
pbet = plot.areabetween(x,yhigh,ylow,legend = 'Range',color = BLUE,alpha = 0.2)
pmat = plot.line(x,mat,legend = 'Matches',color = RED)
pmat2 = plot.line(x,mat,color = RED,legend = None)
## need to duplicate if want to plot the same thing.
plot.displaysubplots([[[pave],[pbet]],[[pmat2],[pmat]]],'examplegraph',title = 'Example savings',
             ylabel = 'Savings $',ylabels = ['hap\npy','bear'],legendtitle = 'title')




