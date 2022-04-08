from osgeo import gdal
import glob as glob

# stack (concatenate in time)
path = './data/'
year = '2017'
tile = '2_4'
imlist = list(sorted(glob.glob(path+'L'+year+'*'+tile+'.tif')))

vrt = 'output_'+tile+'_'+year+'.vrt'

gdal.Translate('tile_'+tile+'_'+year+'.tif',gdal.BuildVRT(vrt,imlist,separate=True,callback=gdal.TermProgress_nocb),format='GTiff',creationOptions=['COMPRESS:DEFLATE','TILES:YES'],callback=gdal.TermProgress_nocb)

# merge to mosaic (merge tiles)
# the below two methods make the file too large (GBs)
# only the gdal_merge.py gives an appropriate size

#gdal_merge.py -o mosaic_2019.tif -co COMPRESS=DEFLATE tile*2019.tif
