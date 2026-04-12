from setuptools import setup
import setup_translate

pkg = 'Extensions.mspFS'
setup(name='enigma2-plugin-extensions-mspfs',
       version='3.0',
       description='mspFS for Enigma2',
       package_dir={pkg: 'mspFS'},
       packages=[pkg],
       package_data={pkg: ['picons/*.png', 'vkb_mod_image/*.png', '*.png', 'locale/*/LC_MESSAGES/*.mo', 'LICENSE']},
       cmdclass=setup_translate.cmdclass,  # for translation
      )
