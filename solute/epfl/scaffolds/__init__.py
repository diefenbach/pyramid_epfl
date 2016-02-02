from pyramid.scaffolds import PyramidTemplate


class EPFLStarterTemplate(PyramidTemplate):
    _template_dir = 'epfl_starter_scaffold'
    summary = 'EPFL starter application'


class EPFLTutorialTemplate(PyramidTemplate):
    _template_dir = 'epfl_tutorial_scaffold'
    summary = 'EPFL tutorial application'
