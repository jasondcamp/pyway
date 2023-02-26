from pyway.helpers import Utils

class Migration():
    def __init__(self, version, extension, name, checksum, apply_timestamp):
        self.version = version
        self.extension = extension
        self.name = name
        self.checksum = checksum
        self.apply_timestamp = apply_timestamp

    @classmethod
    def from_name(cls, name, **kwargs):
        version = kwargs.get('version', Utils.get_version_from_name(name))
        extension = kwargs.get('extension', Utils.get_extension_from_name(name))
        checksum = kwargs.get('checksum', Utils.load_checksum_from_name(name))
        apply_timestamp = kwargs.get('apply_timestamp')
        return cls(version, extension, name, checksum, apply_timestamp)

    @classmethod
    def from_list(cls, list_):
        return [cls(m.version, m.extension, m.name, m.checksum, m.apply_timestamp) for m in list_]

    @classmethod
    def from_list_names(cls, list_):
        return [cls.from_name(m.name) for m in list_]
