import pandas as pd
import matplotlib.pyplot as plt
import mpld3

if __name__ == "__main__":
    import numpy as np
    
    fig = plt.figure(figsize = (18,8))

    # generate 10 random x,y values
    x = np.random.rand(10)
    y = np.random.rand(10)

    # create a scatter plot of the points
    plt.scatter(x, y)

    # add labels and a title
    plt.xlabel('X values')
    plt.ylabel('Y values')
    plt.title('10 Random X,Y Values')
    
    html_str = mpld3.fig_to_html(fig)
    Html_file= open("index.html","w")
    Html_file.write(html_str)
    Html_file.close()
