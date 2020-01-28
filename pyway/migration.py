from .helpers import Utils


class Migration():

    def __init__(self, version, extension, name, checksum):
        self.version = version
        self.extension = extension
        self.name = name
        self.checksum = checksum

    @classmethod
    def from_name(cls, name, **kwargs):
        version = kwargs.get('version', Utils.get_version_from_name(name))
        extension = kwargs.get('extension', Utils.get_extension_from_name(name))
        checksum = kwargs.get('checksum', Utils.load_checksum_from_name(name))
        return cls(version, extension, name, checksum)

    @classmethod
    def from_list(cls, list_):
        return [cls(m.version, m.extension, m.name, m.checksum) for m in list_]

    @classmethod
    def from_list_names(cls, list_):
        return [cls.from_name(m.name) for m in list_]

    def __repr__(self):
        return 'Migration(version=%s, extension=%s, name=%s, checksum=%s)' % \
            (self.version, self.extension, self.name, self.checksum)
