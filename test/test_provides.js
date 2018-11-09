const assert = require('assert');
const fs = require('fs');
const path = require('path');
const tmp = require('tmp');
tmp.setGracefulCleanup();

const prov = require('../rpm/npmlib.prov');

function makeModulesDir() {
  var tmpdir = tmp.dirSync();
  var modulesDir = path.join(tmpdir.name, 'node_modules');
  fs.mkdirSync(modulesDir);
  return modulesDir;
}

describe('auto-provides', function () {
  it('should return the name and version from a package.json', function() {
    const testData = {
      name: "test-package",
      version: "1.2.3"
    };
    assert.equal(prov.processPackageJSON(testData), "npmlib(test-package) = 1.2.3\n");

  });
});

describe('bundled provides', function() {
  it('should detect bundled dependencies', function () {
    var modulesDir = makeModulesDir();
    fs.mkdirSync(path.join(modulesDir, 'test-module'));
    fs.writeFileSync(path.join(modulesDir, 'test-module', 'package.json'),
      JSON.stringify({name: 'test-module', version: '3.4.5'}));

    assert.equal(prov.processBundledDeps(path.join(modulesDir, '..')),
      'bundled(npmlib(test-module)) = 3.4.5\n');
  });

  it('should skip modules with no dependencies', function() {
    var moduleDir = tmp.dirSync();
    assert.equal(prov.processBundledDeps(moduleDir.name), '');
  });

  it ('should skip non-bundled dependencies', function() {
    var moduleDir = makeModulesDir();
    fs.symlinkSync('/usr/lib/npm-library/whatever/1.0.0', path.join(moduleDir, 'whatever'));
    assert.equal(prov.processBundledDeps(path.join(moduleDir, '..')), '');
  });
});
