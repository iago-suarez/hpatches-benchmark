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
    # 'sift': Descriptor(name='SIFT', color='seagreen'),
    'sift': Descriptor(name='SIFT', color='hotpink'),
    'rootsift': Descriptor(name='RSIFT', color='olive'),
    'orb': Descriptor(name='ORB', color='skyblue'),
    'brief': Descriptor(name='BRIEF', color='darkcyan'),
    'binboost': Descriptor(name='BinBoost', color='steelblue'),
    'tfeat-liberty': Descriptor(name='TFeat-LIB', color='teal'),
    'geodesc': Descriptor(name='GeoDesc', color='tomato'),
    'hardnet-liberty': Descriptor(name='HNet-LIB', color='chocolate'),
    'hardnet+': Descriptor(name='Hardnet', color='lightgray'),
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
    'Ada50p_512_AverageBoxThresholdedWL': Descriptor(name='Ada512p50', color='pink'),
    'Ada50p_lr0.1_512_AverageBoxThresholdedWL': Descriptor(name='Ada512p50', color='pink'),
    'Ada20p_512_AverageBoxThresholdedWL': Descriptor(name='UnbAda512p20', color='pink'),
    'Ada20p_lr0.1_512_AverageBoxThresholdedWL': Descriptor(name='Ada512p20', color='pink'),
    'Ada10p_512_AverageBoxThresholdedWL': Descriptor(name='UnbAda512p10', color='pink'),
    'Ada05p_512_AverageBoxThresholdedWL': Descriptor(name='UnbAda512p05', color='pink'),
    'Ada05p_lr0.1_512_AverageBoxThresholdedWL': Descriptor(name='Ada512p05', color='pink'),
    'Ada01p_512_AverageBoxThresholdedWL': Descriptor(name='UnbAda512p01', color='pink'),
    'BELID-U-ADA_512_AverageBoxThresholdedWL': Descriptor(name='BELID-U-ADA-512', color='pink'),
    'EasyBEBLID_260_AverageBoxThresholdedWL': Descriptor(name='EasyBEBLID260', color='blue'),
    'LibBEBLID_256_AverageBoxThresholdedWL': Descriptor(name='BEBLID260', color='blue'),
    'UnbBEBLID_63_AverageBoxThresholdedWL': Descriptor(name= 'BEBLID-63-M', color='blue'),
    'UnbBEBLID_96_AverageBoxThresholdedWL': Descriptor(name= 'BEBLID-96-M', color='blue'),
    'UnbBEBLID_206_AverageBoxThresholdedWL': Descriptor(name='BEBLID-206-M', color='blue'),
    'UnbBEBLID_242_AverageBoxThresholdedWL': Descriptor(name='BEBLID-242-M', color='blue'),
    'UnbBEBLID_259_AverageBoxThresholdedWL': Descriptor(name='BEBLID-259-M', color='blue'),
    'UnbBEBLID_279_AverageBoxThresholdedWL': Descriptor(name='BEBLID-279-M', color='blue'),
    'UnbBEBLID_304_AverageBoxThresholdedWL': Descriptor(name='BEBLID-304-M', color='blue'),
    'UnbBEBLID_512_AverageBoxThresholdedWL': Descriptor(name='BEBLID-512-M', color='blue'),
    'BEBLID_512_AverageBoxThresholdedWL': Descriptor(name='BEBLID-512-M', color='blue'),
    'BEBLID_256_AverageBoxThresholdedWL': Descriptor(name='BEBLID-256', color='blue'),
    'BEBLID_p20_512_AverageBoxThresholdedWL': Descriptor(name='BEBLID-512-M', color='blue'),
    'BEBLID_p50_512_AverageBoxThresholdedWL': Descriptor(name='BEBLID512p50', color='blue'),
    'Lib200kBEBLID_512_AverageBoxThresholdedWL': Descriptor(name='BEBLID-512-V', color='blue'),
    'BEBLID_P50_256_AverageBoxThresholdedWL': Descriptor(name='BEBLID-256-V', color='blue'),
    'BEBLID_P50_512_AverageBoxThresholdedWL': Descriptor(name='BEBLID-512-V', color='blue'),
    'UnbBEBLIDCrop304_256_AverageBoxThresholdedWL': Descriptor(name='UnbBEBLID256Crop', color='blue'),
    'BEBLID_278_AverageBoxThresholdedWL': Descriptor(name='BEBLID278', color='blue'),
    'BEBLID_p05_512_AverageBoxThresholdedWL': Descriptor(name='BEBLID512p05', color='blue'),
    'BEBLID_476_AverageBoxThresholdedWL': Descriptor(name='BEBLID476p20', color='blue'),
    'ForcedBEBLIDp20_512_AverageBoxThresholdedWL': Descriptor(name='Ada512-w1-p20', color='gold'),
    'ForcedBEBLIDp05_512_AverageBoxThresholdedWL':Descriptor(name='Ada512-w1-p5', color='gold'),
    'BEBLID_512_GradientBasedWL': Descriptor(name='BEBLID-Grad', color='gold'),
    # Ablation Study
    'cvLATCH-256': Descriptor(name='cvLATCH-256', color='navy'),
    'VedaldiSIFT2': Descriptor(name='VedaldiSIFT2', color='red'),
    '100k_hinge_t1.0_lr0.05_GTBB_256_AverageBoxThresholdedWLv2': Descriptor(name='GTBB-256', color='deeppink'),
    'HashSIFT_sh0.024_lr0.0002_SIFT_kp_scale=0.1250,_sigma=0.7_256_SIFT_kp_scale=0.1250,_sigma=0.7': Descriptor(name='HashSIFT-256', color='crimson'),
    'HashSIFT_sh0.012_lr0.0002_SIFT_kp_scale=0.1250,_sigma=0.7_512_SIFT_kp_scale=0.1250,_sigma=0.7': Descriptor(name='HashSIFT-512', color='crimson'),
    'BoxDiffs_(256)': Descriptor(name='BoxDiffs', color='green'),
    '32x32-CDbin-256': Descriptor(name='32x32-CDbin-256b', color='grey'),
    '64x64-CDbin-256': Descriptor(name='CDbin-256b', color='grey'),
    'ConvOpt-120': Descriptor(name='ConvOpt-120', color='green'),
    'Aug_10K_ABD_HNM256_lr0.03_512_AverageBoxThresholdedWLv2':  Descriptor(name='BAD-512', color='aqua'),
    'Aug_20K_BAD_HNM256_lr0.04_256_AverageBoxThresholdedWLv2':  Descriptor(name='BAD-256', color='aqua'),
    'LDAHashDIF128': Descriptor(name='LDAHash-DIF-128', color='peru'),
    'LDAHashLDA128': Descriptor(name='LDAHash-LDA-128', color='peru'),
    'cvORB': Descriptor(name='cvORB', color='skyblue'),
    'cvRSIFT': Descriptor(name='RSIFT', color='orange'),
    'cvFREAK': Descriptor(name='FREAK', color='slateblue'),
    'cvBRISK': Descriptor(name='BRISK', color='lightseagreen'),
    'cvLATCH': Descriptor(name='LATCH-512', color='navy'),
    'cvLUCID': Descriptor(name='cvLUCID', color='yellow'),
    'BaseORB2': Descriptor(name='BaseORB', color='skyblue'),
    'HashORB_SiftLikeBoxDiffs_(256)_256_SiftLikeBoxDiffs_(256)': Descriptor(name='HashORB', color='royalblue'),
    'ORB_in_BEBLID_format_256_AverageBoxThresholdedWL': Descriptor(name='XmlORB', color='skyblue'),
    'SOSNet': Descriptor(name='SOSNet', color='lightgray'),
    'tfeat-margin-star': Descriptor(name='Tfeat-m*', color='#222222'),
    'DOAP-Lib-256b': Descriptor(name='DOAP-Lib-256b', color='goldenrod'),
    'DOAP-ST-Lib-256b': Descriptor(name='DOAP-ST-256b', color='#eeeeee'),
    'HashSIFT-256': Descriptor(name='HashSIFT-256', color='crimson'),
    'DOAP-Lib-128f': Descriptor(name='DOAP-Lib-128f', color='gold'),
    'DOAP-Lib-128f-NoNorm': Descriptor(name='DOAP-Lib-128f-NoNorm', color='gold'),
    'HashSIFT_sh0.024_lr0.0002-256': Descriptor(name='HashSIFT-256', color='crimson'),
    'HashSIFT_sh0.012_lr0.0002-512': Descriptor(name='HashSIFT-512', color='crimson'),
    'BAD_512_AverageBoxThresholdedWLv2': Descriptor(name='BAD-512', color='aqua'),
    'BAD_256_AverageBoxThresholdedWLv2': Descriptor(name='BAD-256', color='aqua'),
    'AugBAD_512_AverageBoxThresholdedWLv2': Descriptor(name='AugBAD-512', color='aqua'),
    'AugBAD_256_AverageBoxThresholdedWLv2': Descriptor(name='AugBAD-256', color='aqua'),
    'LDB': Descriptor(name='LDB', color='teal'),
    'BiSIFT': Descriptor(name='BiSIFT', color='orangered'),
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
