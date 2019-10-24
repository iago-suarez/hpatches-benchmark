"""Code for configuring the appearance of the HPatches results figure.

For each descriptor, a name and a colour that will be used in the
figure can be configured.

You can add new descriptors as shown example below:
'desc':
Descriptor(name='Desc++', color='darksalmon'),

This will add a new descriptor, using the results from the `desc`
folder, with name appearing in the figure as `Desc++`, and
darksalmon colour.

The colour string, has to be a valid names colour, from the following
list:
https://matplotlib.org/examples/color/named_colors.html

Note that `new_descriptor` should match the name of the folder
containing the HPatches results.
"""
import collections

Descriptor = collections.namedtuple('Descriptor', 'name color')
desc_info = {
    'sift': Descriptor(name='SIFT', color='seagreen'),
    'rootsift': Descriptor(name='RSIFT', color='olive'),
    'orb': Descriptor(name='ORB', color='skyblue'),
    'brief': Descriptor(name='BRIEF', color='darkcyan'),
    'binboost': Descriptor(name='BinBoost', color='steelblue'),
    'tfeat-liberty': Descriptor(name='TFeat-LIB', color='teal'),
    'geodesc': Descriptor(name='GeoDesc', color='tomato'),
    'hardnet-liberty': Descriptor(name='HNet-LIB', color='chocolate'),
    'hardnet+': Descriptor(name='Hardnet+', color='chocolate'),
    'deepdesc-ubc': Descriptor(name='DDesc-LIB', color='black'),
    'NCC': Descriptor(name='LearnedSIFT', color='blue'),
    'misigma': Descriptor(name='MeanStd', color='red'),
    'BoostedSSC_512_AverageBoxThresholdedWL': Descriptor(name='BELID-U-512', color='green'),
    'Adaboost_512_AverageBoxThresholdedWL': Descriptor(name='ADA-512', color='pink'),
    'BELID_512': Descriptor(name='BELID-512', color='green'),
    'BELID_256': Descriptor(name='BELID-256', color='green'),
    'BELID_128': Descriptor(name='BELID-128', color='green'),
    'ADA-512-HPATHCES': Descriptor(name='Ada512HAll', color='pink'),
    'ADA-512-HPATCHES-EASY': Descriptor(name='Ada512HEasy', color='pink'),
    'ADA-512-HPATCHES-EASY2': Descriptor(name='Ada512HEasy2', color='pink'),
    'EasyAdaboost_512_AverageBoxThresholdedWL': Descriptor(name='EasyAda512', color='pink'),
    'LibAdaboost_512_AverageBoxThresholdedWL': Descriptor(name='LibAda512', color='pink'),
    'Lib200KAda_512_AverageBoxThresholdedWL': Descriptor(name='LibAda200K512', color='pink'),
    'FPBoostMatrix-Adaboost_512-512_AverageBoxThresholdedWL': Descriptor(name='EasyFPBooAda512', color='green'),
    'Ada05p_512_AverageBoxThresholdedWL': Descriptor(name='UnbAda512p05', color='pink'),
    'Ada10p_512_AverageBoxThresholdedWL': Descriptor(name='UnbAda512p10', color='pink'),
    'Ada20p_512_AverageBoxThresholdedWL': Descriptor(name='UnbAda512p20', color='pink'),
    'Ada01p_512_AverageBoxThresholdedWL': Descriptor(name='UnbAda512p01', color='pink'),
    'EasyBEBLID_260_AverageBoxThresholdedWL': Descriptor(name='EasyBEBLID260', color='blue'),
    'LibBEBLID_256_AverageBoxThresholdedWL': Descriptor(name='BEBLID260', color='blue'),
    'UnbBEBLID_242_AverageBoxThresholdedWL': Descriptor(name='BEBLID242p20', color='blue'),
    'UnbBEBLID_206_AverageBoxThresholdedWL': Descriptor(name='BEBLID206p20', color='blue'),
    'UnbBEBLID_63_AverageBoxThresholdedWL': Descriptor(name= 'BEBLID63p20', color='blue'),
    'UnbBEBLID_304_AverageBoxThresholdedWL': Descriptor(name='BEBLID304p20', color='blue'),
    'UnbBEBLID_512_AverageBoxThresholdedWL': Descriptor(name='BEBLID512p20', color='blue'),
    'BEBLID_p20_512_AverageBoxThresholdedWL': Descriptor(name='BEBLID512p20', color='blue'),
    'UnbBEBLIDCrop304_256_AverageBoxThresholdedWL': Descriptor(name='UnbBEBLID256Crop', color='blue'),
    'BEBLID_278_AverageBoxThresholdedWL': Descriptor(name='BEBLID278', color='blue'),
    'BEBLID_p05_512_AverageBoxThresholdedWL': Descriptor(name='BEBLID512p05', color='blue'),
    # Add you own descriptors as below:
    # 'desc':
    # Descriptor(name='Desc++', color='darksalmon'),
}

# Symbols for the figure
figure_attributes = {
    'intra_marker': ".",
    'inter_marker': "d",
    'viewp_marker': "*",
    'illum_marker': r"$\diamond$",
    'easy_colour': 'green',
    'hard_colour': "purple",
    'tough_colour': "red",
}
