/* eslint-env mocha */
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const tmp = require('tmp');

tmp.setGracefulCleanup();

const req = require('../rpm/npmlib.req');

function makeModulesDir() {
  const tmpdir = tmp.dirSync();
  const modulesDir = path.join(tmpdir.name, 'node_modules');
  fs.mkdirSync(modulesDir);
  return modulesDir;
}

describe('auto-requires.processDependency', () => {
  it('should convert a symlink to a requirement', () => {
    const modulesDir = makeModulesDir();
    fs.symlinkSync('/usr/lib/npm-library/test-modules/1.2.3',
      path.join(modulesDir, 'test-module'));

    assert.equal(req.processDependency(path.join(modulesDir, '..'), 'test-module'),
      'npmlib(test-module) = 1.2.3\n');
  });

  it('should throw an error on a missing symlink', () => {
    const modulesDir = makeModulesDir();
    assert.throws(() => {
      req.processDependency(path.join(modulesDir, '..'), 'test-module');
    });
  });
});

describe('auto-requires.processJSON', () => {
  it('should walk all package.json dependencies', () => {
    const modulesDir = makeModulesDir();
    fs.symlinkSync('/usr/lib/npm-library/test-modules/1.2.3',
      path.join(modulesDir, 'test-module-1'));
    fs.symlinkSync('/usr/lib/npm-library/test-modules/2.4.5',
      path.join(modulesDir, 'test-module-2'));

    const testData = {
      dependencies: {
        'test-module-1': '^1.0.0',
        'test-module-2': '^2.0.0',
      },
    };

    const testResult = 'nodejs(engine)\n'
      + 'npmlib(test-module-1) = 1.2.3\n'
      + 'npmlib(test-module-2) = 2.4.5\n';

    assert.equal(req.processPackageJSON(path.join(modulesDir, '..', 'package.json'), testData),
      testResult);
  });
});
