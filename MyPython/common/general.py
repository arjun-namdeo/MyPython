#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
General module with common functional procedures
"""
import os
from my_python import constants
from logIO import get_logger

logger = get_logger(__name__)


class PyProject(object):
    """
    A simple class for which contains attribute related to a specific project
    """
    def __init__(self, name, root_path):
        self.name = str(name)
        self.root_path = str(root_path)

    @property
    def is_source_package(self):
        return constants.PY_SOURCE_DIR in self.root_path

    @property
    def is_build_package(self):
        return constants.PY_BUILDS_DIR in self.root_path

    @property
    def is_testing_package(self):
        return constants.PY_TESTING_DIR in self.root_path

    def get_requirements_file(self):
        """
        Get the requirements file if any for the project, Returns None if nothing.

        :return             `str`           Requirements file path if found else None
        """
        req_file = os.path.join(self.root_path, constants.requirements_file)
        if os.path.isfile(req_file):
            return req_file
        logger.debug("Cannot find requirements file for '{0}' project.".format(self.name))
        return None

    def get_package_setup_file(self):
        """
        Get the package_setup file if any for the project, Returns None if nothing.

        :return             `str`           package_setup file path if found else None
        """
        setup_file = os.path.join(self.root_path, constants.package_setup_file)
        if os.path.isfile(setup_file):
            return setup_file
        logger.error("Cannot find package_setup file for '{0}' project.".format(self.name))
        return None

    def setup_project(self):
        """
        This method should basically read the package_setup and update the env_paths
        respectively.

        Also just a note, We need to make this compatible for cross platform uses i.e. for Windows/Linux/Mac
        """
        raise NotImplementedError("This have not been implemented yet. But I need to do it sometime later.")


def get_project_root_from_path(source_path):
    """
    Generic method to get the project root path from given path. The func can be really handy
    for all the projects as you can get the project root directory from a given path

    i.e.
        Lets assume you have a path where your files are there

        /local/scm_tools/src/
                            /scm_tools
                                /__init__.py
                                /common.py


        Now you'd want to know the root directory of project for many reason such as get the
        package_setup.py file, read the requirement.txt file etc.

        With this method you can pass any of following paths and It will return you the PyProject object which
        contains lots of useful attributes.

    :param source_path:         `str`                       AbsPath for the project
    :return:                    `PyProjectInstance`         PyProject Instance for given path of found else None
    """
    def _get_root_directory(src_path, path_checked=None):
        path_checked = list() if path_checked is None else path_checked
        if src_path is None or not os.path.exists(src_path):
            return None

        if src_path in path_checked:
            # It's repeating this path, If this path was root directory, The function would have returned the
            # path so no need to waste checking it again.
            return None

        if os.path.isfile(src_path):
            src_path = os.path.dirname(src_path)

        if constants.package_setup_file in os.listdir(src_path):
            return src_path

        path_checked.append(src_path)
        return _get_root_directory(src_path=os.path.dirname(src_path), path_checked=path_checked)

    root_path = _get_root_directory(src_path=source_path)
    if root_path is None:
        logger.warning("Given path is not a valid project.")
        return None

    root_name = os.path.basename(root_path)
    return PyProject(name=root_name, root_path=root_path)


_fast_key_list = {'_asset', '_entity', '_seq', '_show', '_shot', '_step', '_task', '_sg_task', '_task_context',
                  'asset', 'asset_type', 'entity_path', 'in_asset', 'in_shot', 'in_seq', 'location', 'seq', 'shot',
                  'show', 'show_follows_tasks', 'step', 'task', 'task_path', 'raw_task_path'}


class ContextDict(dict):
    '''A special dictionary that knows how to self-populate certain pipeline elements on demand.'''

    def __init__(self, task_context):
        '''All the information that this object looks up is based on either the environment. However,
        note that many of the pipeline items are based on the BFX_ENTITY_ID environment variable. If
        you want a context that is not based on that, just set the given value in the dictionary before
        any lookups happen.

        Note: it returns None whenever it cannot generate the required item. It doesn't raise a KeyError
        exception unless the item is not an auto-generate item.'''
        super(ContextDict, self).__init__()

        self['_entity'] = task_context.entity
        self['_task_context'] = task_context
        self['task_path'] = task_context.task_path
        self['raw_task_path'] = task_context.raw_task_path

    def __getitem__(self, item):
        # Override this so that C[X] can generate the required items.
        if item in _fast_key_list or item.startswith('$'):
            if not super(ContextDict, self).__contains__(item):
                self[item] = self._generate_item(item)
        return super(ContextDict, self).__getitem__(item)

    def __contains__(self, item):
        # Override this so that X in C returns True, even if it hasn't been generated yet.
        if item in _fast_key_list or item.startswith('$'):
            return True
        super(ContextDict, self).__contains__(item)

    def get_presets(self):
        return self['_task_context'].get_presets(context=self, name='presets')

    def pre_cache_items(self):
        '''
        Sometimes the lazy evaluation of this class is a problem. In such cases, we need to call this
        method to pre-cache the item evaluations for all the values. For example, if you're trying
        to use this as an argument to a format call.
        '''

        for item in _fast_key_list:
            self.__getitem__(item)
        for item in os.environ:
            self.__getitem__('$'+item)

    def _generate_item(self, item):
        """
        Hidden function that is called only when someone has requested an item that we know we
        can auto-generate and that hasn't already been computed. It returns the generated item.
        """
        if item.startswith('$'):
            try:
                return os.environ[item[1:]]
            except KeyError:
                return None

        if item == '_entity':
            id = self['$BFX_ENTITY_ID']
            if id is None:
                return None

            return id

        if item == '_show':
            entity = self['_entity']
            if entity is None:
                return None
            return entity.get_root()

        if item == '_sg_task':
            task_context = self['_task_context']
            return task_context.get_sg_task()

        if item == '_task':
            if not self['show_follows_tasks']:
                return None
            entity = self['_entity']
            if entity is None:
                return None
            if entity.shotgun_model.model_class_name == 'Task':
                return entity
            return None

        if item == '_step':
            assert self['_sg_task']   # TODO add support for DT shows
            task = self['_sg_task']
            if task is None:
                return None
            return task.step

        if item == 'show':
            entity = self['_show']
            if entity is None:
                return None
            return entity.name

        if item == 'task':
            sg_task = self['_sg_task']
            if sg_task is None:
                return None
            return sg_task.name

        if item == 'step':
            step = self['_step']
            if step is None:
                return None
            return step.short_name.lower()

        if item == '_asset':
            entity = self['_entity']
            while entity is not None:
                sg_entity = entity.shotgun_model
                if sg_entity and sg_entity.model_class_name == 'Asset':
                    return entity
                entity = entity.parent if entity.parent_id else None
            return None

        if item == '_shot':
            entity = self['_entity']
            while entity is not None:
                sg_entity = entity.shotgun_model
                if sg_entity and sg_entity.model_class_name == 'Shot':
                    return entity
                entity = entity.parent if entity.parent_id else None
            return None

        if item == '_seq':
            entity = self['_entity']
            while entity is not None:
                sg_entity = entity.shotgun_model
                if sg_entity and sg_entity.model_class_name == 'Sequence':
                    return entity
                entity = entity.parent if entity.parent_id else None
            return None

        if item == 'asset_type':
            asset = self['_asset']
            if asset is None:
                return None
            else:
                return asset.shotgun_model.type_short

        if item == 'shot':
            shot = self['_shot']
            if shot is None:
                return None
            return shot.name

        if item == 'seq':
            seq = self['_seq']
            if seq is None:
                return None
            return seq.name

        if item == 'in_seq':
            seq = self['_seq']
            return seq is not None

        if item == 'in_shot':
            shot = self['_shot']
            return shot is not None

        if item == 'asset':
            asset = self['_asset']
            if asset is None:
                return None
            return asset.name

        if item == 'entity_path':
            entity = self['_entity']
            return entity.get_full_name()

