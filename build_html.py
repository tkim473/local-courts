from court_calc import plot_pickle
import base64
from io import BytesIO


fig, axs = plot_pickle()

tmpfile = BytesIO()
fig.savefig(tmpfile, format='png')
encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')

plot_html = '<html>' + '<img src=\'data:image/png;base64,{}\'>'.format(encoded) + '</html>'

with open('index.html','w') as f:
    f.write(plot_html)