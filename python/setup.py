from distutils.core import setup
from distutils.core import Extension

mmh3module = Extension('mmh3', sources=['mmh3/mmh3module.cpp', 'mmh3/MurmurHash3.cpp'])


setup(
    name='PlanOut',
    version='0.5',
    author='Facebook, Inc.',
    author_email='eytan@fb.com',
    packages=[
        'planout',
        'planout.ops',
        'planout.test',
        'planout.optimizely',
        'planout.optimizely.ops',
        'planout.optimizely.test',
    ],
    url='http://pypi.python.org/pypi/PlanOut/',
    ext_modules = [mmh3module],
    license='LICENSE',
    description='PlanOut is a framework for online field experimentation.',
    keywords=['experimentation', 'A/B testing'],
    long_description="""PlanOut is a framework for online field experimentation.
    PlanOut makes it easy to design both simple A/B tests and more complex
    experiments, including multi-factorial designs and within-subjects designs.
    It also includes advanced features, including built-in logging, experiment
    management, and serialization of experiments via a domain-specific language.
    """
)

# long_description=open('README.md').read(),
