import os

import sublime


class VcsHelper(object):
    @classmethod
    def vcs_dir(cls, directory):
        """Return the path to the metadata directory, assuming it is
        directly under the passed directory."""
        if not directory:
            return False

        directory_list = []

        for meta_data_directory in cls.meta_data_directory():
            directory_list.append(os.path.join(directory, meta_data_directory))

        return directory_list

    @classmethod
    def vcs_file_path(cls, view, vcs_path):
        """Returns the relative path to the file in the Sublime view, in
        the repository rooted at vcs_path."""
        if not vcs_path:
            return False
        full_file_path = os.path.realpath(view.file_name())
        vcs_path_to_file = \
            full_file_path.replace(vcs_path, '').replace('\\', '/')
        if vcs_path_to_file[0] == '/':
            vcs_path_to_file = vcs_path_to_file[1:]
        return vcs_path_to_file

    @classmethod
    def vcs_root(cls, directory):
        """Returns the top-level directory of the repository."""
        for meta_data_directory in cls.meta_data_directory():
            if (os.path.exists(os.path.join(directory, meta_data_directory))):
                return directory

        parent = os.path.realpath(os.path.join(directory, os.path.pardir))
        if parent == directory:
            # we have reached root dir
            return False
        else:
            return cls.vcs_root(parent)

    @classmethod
    def vcs_tree(cls, view):
        """Returns the directory at the top of the tree that contains
        the file in the passed Sublime view."""
        full_file_path = view.file_name()
        file_parent_dir = os.path.realpath(os.path.dirname(full_file_path))
        return cls.vcs_root(file_parent_dir)

    @classmethod
    def is_repository(cls, view):
        if view is None or view.file_name() is None:
            return False
        else:
            vcs_dir_list = cls.vcs_dir(cls.vcs_tree(view))

            if not vcs_dir_list:
                return False

            for directory in vcs_dir_list:
                if directory:
                    return True
                    
            return False


class GitHelper(VcsHelper):
    @classmethod
    def meta_data_directory(cls):
        return ['.git']

    @classmethod
    def is_git_repository(cls, view):
        return cls.is_repository(view)


class HgHelper(VcsHelper):
    @classmethod
    def meta_data_directory(cls):
        return ['.hg']

    @classmethod
    def is_hg_repository(cls, view):
        return cls.is_repository(view)


class SvnHelper(VcsHelper):
    @classmethod
    def meta_data_directory(cls):
        return ['.svn']

    @classmethod
    def is_svn_repository(cls, view):
        return cls.is_repository(view)

class FossilHelper(VcsHelper):
    @classmethod
    def meta_data_directory(cls):
        return ['.fslckout', '_FOSSIL_']

    @classmethod
    def is_fossil_repository(cls, view):
        return cls.is_repository(view)
