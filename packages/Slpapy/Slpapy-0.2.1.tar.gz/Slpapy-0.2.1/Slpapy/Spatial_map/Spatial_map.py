from .scatterplots import embedding
def Spatial_map(adata, cls):
    cls = str(cls)
    embedding(adata, basis='X_spacial', color=f'{cls}', frameon=False, save=f'_spacial_{cls}.png')






    """
    如需原始比例则在embedding 458行后加上
    axs.axis('equal')
    """