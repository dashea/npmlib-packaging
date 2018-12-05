/* eslint-env mocha */
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const tmp = require('tmp');

tmp.setGracefulCleanup();

const req = require('../rpm/npmlib.req');

function makeModulesDir() {
  const tmpdir = tmp.dirSync({ unsafeCleanup: true });
  const modulesDir = path.join(tmpdir.name, 'node_modules');
  fs.mkdirSync(modulesDir);
  return modulesDir;
}

function uniq(arr) {
  arr.sort();
  return arr.filter((a, idx) => !(arr[idx + 1] === a));
}

describe('auto-requires.processDependency', () => {
  it('should convert a symlink to a requirement', () => {
    const modulesDir = makeModulesDir();
    fs.symlinkSync('/usr/lib/npm-library/test-modules/1.2.3',
      path.join(modulesDir, 'test-module'));

    assert.equal(req.processDependency(path.join(modulesDir, '..'), 'test-module'),
      'npmlib(test-module) = 1.2.3');
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
    const packageJSONPath = path.join(modulesDir, '..', 'package.json');
    fs.writeFileSync(packageJSONPath, JSON.stringify(testData));

    const testResult = [
      'nodejs(engine)',
      'npmlib(test-module-1) = 1.2.3',
      'npmlib(test-module-2) = 2.4.5',
    ];

    assert.deepStrictEqual(uniq(req.processPackageJSON(packageJSONPath)), testResult);
  });

  it('should walk bundled module dependencies', () => {
    const modulesDir = makeModulesDir();

    fs.symlinkSync('/usr/lib/npm-library/test-module-1/1.2.3',
      path.join(modulesDir, 'test-module-1'));
    fs.symlinkSync('/usr/lib/npm-library/test-module-2/2.4.5',
      path.join(modulesDir, 'test-module-2'));

    const testData = {
      dependencies: {
        'test-module-1': '^1.0.0',
        'test-module-2': '^2.0.0',
        'test-module-3': '^3.0.0',
      },
    };
    const packageJSONPath = path.join(modulesDir, '..', 'package.json');
    fs.writeFileSync(packageJSONPath, JSON.stringify(testData));

    const subModulesDir = path.join(modulesDir, 'test-module-3', 'node_modules');
    fs.mkdirSync(path.join(modulesDir, 'test-module-3'));
    fs.mkdirSync(subModulesDir);

    fs.symlinkSync('/usr/lib/npm-library/test-module-4/4.5.6',
      path.join(subModulesDir, 'test-module-4'));

    const subTestData = {
      dependencies: {
        'test-module-4': '^4.0.0',
      },
    };
    const subPackageJSONPath = path.join(modulesDir, 'test-module-3', 'package.json');
    fs.writeFileSync(subPackageJSONPath, JSON.stringify(subTestData));

    const testResult = [
      'nodejs(engine)',
      'npmlib(test-module-1) = 1.2.3',
      'npmlib(test-module-2) = 2.4.5',
      'npmlib(test-module-4) = 4.5.6',
    ];

    assert.deepStrictEqual(uniq(req.processPackageJSON(packageJSONPath)), testResult);
  });
});
