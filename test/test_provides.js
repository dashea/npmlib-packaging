const assert = require('assert');
const prov = require('../rpm/npmlib.prov');

describe('auto-provides', function () {
  it('should return the name and version from a package.json', function() {
    const testData = {
      name: "test-package",
      version: "1.2.3"
    };
    assert.equal(prov.processPackageJSON(testData), "npmlib(test-package) = 1.2.3\n");

  });
});
