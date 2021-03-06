#    Copyright (C) 2005 Jeremy S. Sanders
#    Email: Jeremy Sanders <jeremy@jeremysanders.net>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
###############################################################################

"""Module for holding collections of settings."""

from reference import Reference

class Settings(object):
    """A class for holding collections of settings."""

    # differentiate widgets, settings and setting
    nodetype = 'settings'

    def __init__(self, name, descr = '', usertext='', pixmap='',
                 setnsmode='formatting'):
        """A new Settings with a name.

        name: name in hierarchy
        descr: description (for user)
        usertext: name for user of class
        pixmap: pixmap to show in tab (if appropriate)
        setnsmode: type of Settings class, one of
              ('formatting', 'groupedsetting', 'widgetsettings', 'stylesheet')
        """

        self.__dict__['setdict'] = {}
        self.name = name
        self.descr = descr
        self.usertext = usertext
        self.pixmap = pixmap
        self.setnsmode = setnsmode
        self.setnames = []  # a list of names
        self.parent = None

    def copy(self):
        """Make a copy of the settings and its subsettings."""

        s = Settings(
            self.name, descr=self.descr, usertext=self.usertext,
            pixmap=self.pixmap, setnsmode=self.setnsmode )
        for name in self.setnames:
            s.add( self.setdict[name].copy() )
        return s

    def isWidget(self):
        """Is this object a widget?"""
        return False

    def getList(self):
        """Get a list of setting or settings types."""
        return [self.setdict[n] for n in self.setnames]

    def getSettingList(self):
        """Get a list of setting types."""
        return [self.setdict[n] for n in self.setnames
                if not isinstance(self.setdict[n], Settings)]

    def getSettingsList(self):
        """Get a list of settings types."""
        return [self.setdict[n] for n in self.setnames
                if isinstance(self.setdict[n], Settings)]

    def getNames(self):
        """Return list of names."""
        return self.setnames

    def getSettingNames(self):
        """Get list of setting names."""
        return [n for n in self.setnames
                if not isinstance(self.setdict[n], Settings)]

    def getSettingsNames(self):
        """Get list of settings names."""
        return [n for n in self.setnames
                if isinstance(self.setdict[n], Settings)]

    def isSetting(self, name):
        """Is the name a supported setting?"""
        return name in self.setdict

    def add(self, setting, posn = -1, readonly = False, pixmap=None):
        """Add a new setting with the name, or a set of subsettings."""
        name = setting.name
        if name in self.setdict:
            raise RuntimeError, "Name already in settings dictionary"
        self.setdict[name] = setting
        if posn < 0:
            self.setnames.append(name)
        else:
            self.setnames.insert(posn, name)
        setting.parent = self
        
        if pixmap:
            setting.pixmap = pixmap

        if readonly:
            setting.readonly = True
        
    def remove(self, name):
        """Remove name from the list of settings."""

        del self.setnames[ self.setnames.index( name ) ]
        del self.setdict[ name ]
        
    def __setattr__(self, name, val):
        """Allow us to do

        foo.setname = 42
        """

        d = self.__dict__['setdict']
        if name in d:
            d[name].val = val
        else:
            self.__dict__[name] = val

    def __getattr__(self, name):
        """Allow us to do

        print foo.setname
        """

        try:
            s = self.__dict__['setdict'][name]
            if isinstance(s, Settings):
                return s
            return s.val
        except KeyError:
            pass

        try:
            return self.__dict__[name]
        except KeyError:
            raise AttributeError, "'%s' is not a setting" % name

    def __getitem__(self, name):
        """Also allows us to do

        print foo['setname']
        """

        d = self.__dict__['setdict']
        try:
            s = d[name]
            if isinstance(s, Settings):
                return s
            else:
                return s.val
        except KeyError:
            raise KeyError, "'%s' is not a setting" % name

    def __contains__(self, name):
        """Whether settings contains name."""
        return name in self.__dict__['setdict']

    def get(self, name = None):
        """Get the setting variable."""

        if name is None:
            return self
        else:
            return self.setdict[name]

    def getFromPath(self, path):
        """Get setting according to the path given as a list."""

        name = path[0]
        if name in self.setdict:
            val = self.setdict[name]
                
            if len(path) == 1:
                if isinstance(val, Settings):
                    raise ValueError, (
                        '"%s" is a list of settings, not a setting' % name)
                else:
                    return val
            else:
                if isinstance(val, Settings):
                    return val.getFromPath(path[1:])
                else:
                    raise ValueError, '"%s" not a valid subsetting' % name
        else:
            raise ValueError, '"%s" is not a setting' % name

    def saveText(self, saveall, rootname = None):
        """Return the text which would reload the settings.

        if saveall is true, save those which haven't been modified.
        rootname is the part to stick on the front of the settings
        """

        # we want to build the root up if we're not the first item
        # (first item is implicit)
        if rootname is None:
            rootname = ''
        else:
            rootname += self.name + '/'

        text = ''.join( [self.setdict[name].saveText(saveall, rootname)
                         for name in self.setnames] )
        return text

    def readDefaults(self, root, widgetname):
        """Return default values from saved text.

        root is the path of the setting in the db, built up by settings
        above this one

        widgetname is the name of the widget this setting belongs to
        """

        root = '%s/%s' % (root, self.name)
        for s in self.setdict.values():
            s.readDefaults(root, widgetname)

    def linkToStylesheet(self, _root=None):
        """Link the settings within this Settings to a stylesheet.
        
        _root is an internal parameter as this function is recursive."""

        # build up root part of pathname to reference
        if _root is None:
            path = []
            obj = self
            while not obj.parent.isWidget():
                path.insert(0, obj.name)
                obj = obj.parent
            path = ['', 'StyleSheet', obj.parent.typename] + path + ['']
            _root = '/'.join(path)

        # iterate over subsettings
        for name, setn in self.setdict.iteritems():
            thispath = _root + name
            if isinstance(setn, Settings):
                # call recursively if this is a Settings
                setn.linkToStylesheet(_root=thispath+'/')
            else:
                ref = Reference(thispath)
                try:
                    # if the reference resolves, then set it
                    ref.resolve(setn)
                    setn.set(ref)
                    setn.default = ref
                except Reference.ResolveException:
                    pass
