npmlib-packaging
================

This is an attempt to improve the way [npm](https://www.npmjs.com/) modules are
packaged for [Fedora Linux](https://getfedora.org/).

The Problem
-----------

One of the core ideas of npm is that, through sub-dependencies, a single application
or module can depend on more than one version of a module at the same time. A dependency
tree might look something like:

    myProgram-1.0.0
    ├─── depA-1.0.0
    │      └─── depC-1.0.0
    │
    │
    └─── depB-1.0.0
           └─── depC-2.0.0

The version conflict is handled by keeping dependencies within the module that
requires them. In the above example, `npm install` will create a directory structure
something like:

    myProgram/
      node_modules/
        depA/
          node_modules/
            depC/ (1.0.0)
        depB/
          node_modules/
            depC/ (2.0.0)

(NB: `npm install` will attempt to flatten the dependency tree, installing
repeated sub-requirements as top-level dependencies. This optimization is unimportant
for our purposes.)

Fedora packages npm modules as RPMs by installing the module data to /usr/lib/node_modules/<module_name>,
creating a node_modules directory within that module for its dependencies, and
creating symlinks in this node_modules directory to the globally installed modules. Something
like:

    /usr/lib/node_modules
      myProgram/
        node_modules/
          depA -> /usr/lib/node_modules/depA
          depB -> /usr/lib/node_modules/depB

As part of this, Fedora does not allow more than version of a module to be installed at
the same time. It doesn't work.

A Solution
----------

### Paths

The obvious thing to change is to stop installing everything to /usr/lib/node_modules. The directory
is indexed by module name (no version), so it obviously cannot support multiple versions simultaneously.
On top of that, making a package available in /usr/lib/node_modules isn't especially useful for
npm. Global modules in /usr/lib/node_modules are not available to `import` or `require`; they still need to
be installed locally. Globally installed modules are available to the `npm link` command, but that's the
only advantage of using that specific directory and that specific layout.

Instead of /usr/lib/node_modules, all modules will be installed to /usr/lib/npm-library/<name>/<version>/.
A package with its dependencies becomes something like:

    /usr/lib/npm-library
      myProgram/
        1.0.0/
          node_modules/
            depA -> /usr/lib/node_modules/depA/1.0.0/
            depB -> /usr/lib/node_modules/depB/1.0.0/
      depA/
        1.0.0/
          node_modules/
            depC -> /usr/lib/node_modules/depC/1.0.0/
      depB/
        1.0.0/
          node_modules/
            depC -> /usr/lib/node_modules/depC/2.0.0/
      depC/
        1.0.0/
        2.0.0/

### Provides and Requires

The automatically generated Provides and Requires metadata uses the form `npmlib(<name>)` to avoid
interfering with existing Fedora packages.

For each dependency, the source package needs a BuildRequires for the given module, using a version
range matching the acceptable versions in package.json. For example, a package.json dependency of
"depA: ^1.0.0" would become "BuildRequires: (npmlib(depA) >= 1.0.0 with npmlib(depA) < 2.0.0)". This
way at least one specific version to link against is available at build time.

During the build, a specific version of each module dependency is linked into the package's node_modules/,
and these specific versions then become the package's Requires metadata. For example, the "depA" dependency
might end up as "Requires: npmlib(depA) = 1.2.3".
