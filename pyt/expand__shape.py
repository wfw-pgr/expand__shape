import numpy                       as np
import nkUtilities.load__pointFile as lpf


# ========================================================= #
# ===  expand__shape                                    === #
# ========================================================= #

def expand__shape():

    xp_, yp_, zp_  = 0, 1, 2
    rf_, zf_       = 0, 1
    fr_, to_       = 0, 1
    
    # ------------------------------------------------- #
    # --- [1] load 1D profile                       --- #
    # ------------------------------------------------- #
    import nkUtilities.load__constants as lcn
    cnsFile = "dat/parameter.conf"
    const   = lcn.load__constants( inpFile=cnsFile )

    Data_list   = []
    for ik in range( const["nFile"] ):
        inpFile = const["file{0:02}".format( ik+1 ) ]
        Data    = lpf.load__pointFile( inpFile=inpFile, returnType="point" )
        Data_list.append( Data )
        
    # ------------------------------------------------- #
    # --- [2] prepare 2D coordinate                 --- #
    # ------------------------------------------------- #
    import nkUtilities.equiSpaceGrid as esg
    x1MinMaxNum = [ float( const["x1MinMaxNum"][0] ), float( const["x1MinMaxNum"][1] ), \
                    int(   const["x1MinMaxNum"][2] ) ]
    x2MinMaxNum = [ float( const["x2MinMaxNum"][0] ), float( const["x2MinMaxNum"][1] ), \
                    int(   const["x2MinMaxNum"][2] ) ]
    x3MinMaxNum = [ 0.0, 0.0, 1 ]
    coord       = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                     x3MinMaxNum=x3MinMaxNum, returnType = "point" )
    radii       = np.sqrt( coord[:,xp_]**2 + coord[:,yp_]**2 )
    theta       = np.arctan2( coord[:,yp_], coord[:,xp_] )
    theta[np.where( theta < 0.0 )] += 2.0 * np.pi
    nCoord      = coord.shape[0]

    # ------------------------------------------------- #
    # --- [3] calculate all interpolated value      --- #
    # ------------------------------------------------- #
    interpolated = np.zeros( (nCoord,const["nFile"]) )
    for ik in range( const["nFile"] ):
        interpolated[:,ik] = np.interp( radii, ( Data_list[ik] )[:,rf_], ( Data_list[ik] )[:,zf_] )
    
    # ------------------------------------------------- #
    # --- [4] get height depending on the theta     --- #
    # ------------------------------------------------- #
    deg2rad  = np.pi / 180.0

    for ik in range( const["nFile"] ):
        th1      = const["th_range.set{0:02}".format( ik+1 )][fr_]*deg2rad
        th2      = const["th_range.set{0:02}".format( ik+1 )][to_]*deg2rad 
        index    = np.where( ( theta >= th1 ) & ( theta <  th2 ) )
        coord[index,zp_] = interpolated[index,ik]
    
    # ------------------------------------------------- #
    # --- [5] draw cmap                             --- #
    # ------------------------------------------------- #
    import nkUtilities.load__config   as lcf
    import nkUtilities.cMapTri        as cmt

    config  = lcf.load__config()
    pngFile = "png/cmap.png"

    config["xTitle"]         = "X (m)"
    config["yTitle"]         = "Y (m)"
    config["cmp_xAutoRange"] = True
    config["cmp_yAutoRange"] = True
    config["cmp_xRange"]     = [-5.0,+5.0]
    config["cmp_yRange"]     = [-5.0,+5.0]

    cmt.cMapTri( xAxis=coord[:,xp_], yAxis=coord[:,yp_], cMap=coord[:,zp_], \
                 pngFile=pngFile, config=config )

    return()
    

# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #
if ( __name__=="__main__" ):
    expand__shape()
