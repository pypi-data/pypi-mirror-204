(self["webpackChunkdcf_widget"] = self["webpackChunkdcf_widget"] || []).push([["lib_index_js"],{

/***/ "./node_modules/css-loader/dist/cjs.js!./css/widget.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./css/widget.css ***!
  \**************************************************************/
/***/ ((module, exports, __webpack_require__) => {

// Imports
var ___CSS_LOADER_API_IMPORT___ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
exports = ___CSS_LOADER_API_IMPORT___(false);
// Module
exports.push([module.id, ".custom-widget {\n  background-color: lightseagreen;\n  padding: 0px 2px;\n}\n", ""]);
// Exports
module.exports = exports;


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ (function(module, exports, __webpack_require__) {

var __WEBPACK_AMD_DEFINE_ARRAY__, __WEBPACK_AMD_DEFINE_RESULT__;// Copyright (c) Paddy Mullen
// Distributed under the terms of the Modified BSD License.
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __exportStar = (this && this.__exportStar) || function(m, exports) {
    for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports, p)) __createBinding(exports, m, p);
};
!(__WEBPACK_AMD_DEFINE_ARRAY__ = [__webpack_require__, exports, __webpack_require__(/*! ./version */ "./lib/version.js"), __webpack_require__(/*! ./widget */ "./lib/widget.js")], __WEBPACK_AMD_DEFINE_RESULT__ = (function (require, exports, version_1, widget_1) {
    "use strict";
    Object.defineProperty(exports, "__esModule", ({ value: true }));
    __exportStar(version_1, exports);
    __exportStar(widget_1, exports);
}).apply(exports, __WEBPACK_AMD_DEFINE_ARRAY__),
		__WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));


/***/ }),

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((module, exports, __webpack_require__) => {

var __WEBPACK_AMD_DEFINE_ARRAY__, __WEBPACK_AMD_DEFINE_RESULT__;// Copyright (c) Paddy Mullen
// Distributed under the terms of the Modified BSD License.
!(__WEBPACK_AMD_DEFINE_ARRAY__ = [__webpack_require__, exports], __WEBPACK_AMD_DEFINE_RESULT__ = (function (require, exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", ({ value: true }));
    exports.MODULE_NAME = exports.MODULE_VERSION = void 0;
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
    // eslint-disable-next-line @typescript-eslint/no-var-requires
    const data = __webpack_require__(/*! ../package.json */ "./package.json");
    /**
     * The _model_module_version/_view_module_version this package implements.
     *
     * The html widget manager assumes that this is the same as the npm package
     * version number.
     */
    exports.MODULE_VERSION = data.version;
    /*
     * The current package name.
     */
    exports.MODULE_NAME = data.name;
}).apply(exports, __WEBPACK_AMD_DEFINE_ARRAY__),
		__WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ (function(module, exports, __webpack_require__) {

var __WEBPACK_AMD_DEFINE_ARRAY__, __WEBPACK_AMD_DEFINE_RESULT__;// Copyright (c) Paddy Mullen
// Distributed under the terms of the Modified BSD License.
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
!(__WEBPACK_AMD_DEFINE_ARRAY__ = [__webpack_require__, exports, __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base"), __webpack_require__(/*! paddy-react-edit-list */ "webpack/sharing/consume/default/paddy-react-edit-list/paddy-react-edit-list"), __webpack_require__(/*! react-dom/client */ "./node_modules/react-dom/client.js"), __webpack_require__(/*! react */ "./node_modules/react/index.js"), __webpack_require__(/*! ./version */ "./lib/version.js"), __webpack_require__(/*! ../css/widget.css */ "./css/widget.css")], __WEBPACK_AMD_DEFINE_RESULT__ = (function (require, exports, base_1, paddy_react_edit_list_1, client_1, react_1, version_1) {
    "use strict";
    Object.defineProperty(exports, "__esModule", ({ value: true }));
    exports.DCFWidgetView = exports.DCFWidgetModel = void 0;
    react_1 = __importDefault(react_1);
    class DCFWidgetModel extends base_1.DOMWidgetModel {
        defaults() {
            return Object.assign(Object.assign({}, super.defaults()), { _model_name: DCFWidgetModel.model_name, _model_module: DCFWidgetModel.model_module, _model_module_version: DCFWidgetModel.model_module_version, _view_name: DCFWidgetModel.view_name, _view_module: DCFWidgetModel.view_module, _view_module_version: DCFWidgetModel.view_module_version, command_config: {}, commands: [] });
        }
    }
    exports.DCFWidgetModel = DCFWidgetModel;
    DCFWidgetModel.serializers = Object.assign({}, base_1.DOMWidgetModel.serializers);
    DCFWidgetModel.model_name = 'DCFWidgetModel';
    DCFWidgetModel.model_module = version_1.MODULE_NAME;
    DCFWidgetModel.model_module_version = version_1.MODULE_VERSION;
    DCFWidgetModel.view_name = 'DCFWidgetView'; // Set to null if no view
    DCFWidgetModel.view_module = version_1.MODULE_NAME; // Set to null if no view
    DCFWidgetModel.view_module_version = version_1.MODULE_VERSION;
    class DCFWidgetView extends base_1.DOMWidgetView {
        constructor() {
            super(...arguments);
            this.setCommandConfig = (conf) => {
                console.log("default setCommandConfig");
            };
        }
        render() {
            this.el.classList.add('custom-widget');
            const root = client_1.createRoot(this.el);
            const widgetModel = this.model;
            const widget = this;
            widgetModel.on('change:command_config', () => { widget.setCommandConfig(widgetModel.get('command_config')); }, this);
            const widgetGetTransformRequester = (setDf) => {
                widgetModel.on('change:transformed_df', () => {
                    setDf(widgetModel.get('transformed_df'));
                }, this);
                const baseRequestTransform = (passedInstructions) => {
                    console.log("transform passedInstructions", passedInstructions);
                    widgetModel.set('commands', passedInstructions);
                    widgetModel.save_changes();
                };
                return baseRequestTransform;
            };
            const widgetGetPyRequester = (setPyCode) => {
                //_.delay(() => setPyCode("padddy"), 200)
                widgetModel.on('change:generated_py_code', () => {
                    const genCode = widgetModel.get('generated_py_code');
                    console.log("gen code", genCode);
                    setPyCode(genCode);
                    //setPyCode("padddy")
                }, this);
                const unusedFunc = (passedInstructions) => {
                    console.log("pyRequester passed instructions", passedInstructions);
                };
                return unusedFunc;
            };
            //this onChange gets called, the one inside of widgetGetPyRequester doesn't get called
            widgetModel.on('change:generated_py_code', () => {
                const genCode = widgetModel.get('generated_py_code');
                console.log("gen code2", genCode);
                //setPyCode(genCode)
                //setPyCode("padddy")
            }, this);
            // widgetModel.on('change:generated_py_error', () => {
            //     console.log("generated_py_error", widgetModel.get('generated_py_error' as string))
            // }, this)
            const commandConfig = widgetModel.get('command_config');
            console.log("widget, commandConfig", commandConfig, widgetModel);
            const plumbCommandConfig = (setter) => {
                widget.setCommandConfig = setter;
            };
            const reactEl = react_1.default.createElement(paddy_react_edit_list_1.WidgetDCFCell, {
                origDf: widgetModel.get('js_df'),
                getTransformRequester: widgetGetTransformRequester,
                commandConfig,
                exposeCommandConfigSetter: plumbCommandConfig,
                getPyRequester: widgetGetPyRequester
                //getPyRequester:(foo:any) => {console.log("getPyRequester called with", foo)}
            }, null);
            root.render(reactEl);
        }
    }
    exports.DCFWidgetView = DCFWidgetView;
}).apply(exports, __WEBPACK_AMD_DEFINE_ARRAY__),
		__WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));


/***/ }),

/***/ "./node_modules/react-dom/client.js":
/*!******************************************!*\
  !*** ./node_modules/react-dom/client.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";


var m = __webpack_require__(/*! react-dom */ "./node_modules/react-dom/index.js");
if (false) {} else {
  var i = m.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED;
  exports.createRoot = function(c, o) {
    i.usingClientEntryPoint = true;
    try {
      return m.createRoot(c, o);
    } finally {
      i.usingClientEntryPoint = false;
    }
  };
  exports.hydrateRoot = function(c, h, o) {
    i.usingClientEntryPoint = true;
    try {
      return m.hydrateRoot(c, h, o);
    } finally {
      i.usingClientEntryPoint = false;
    }
  };
}


/***/ }),

/***/ "./css/widget.css":
/*!************************!*\
  !*** ./css/widget.css ***!
  \************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

var api = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
            var content = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./widget.css */ "./node_modules/css-loader/dist/cjs.js!./css/widget.css");

            content = content.__esModule ? content.default : content;

            if (typeof content === 'string') {
              content = [[module.id, content, '']];
            }

var options = {};

options.insert = "head";
options.singleton = false;

var update = api(content, options);



module.exports = content.locals || {};

/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

"use strict";
module.exports = JSON.parse('{"name":"dcf-widget","version":"0.1.0","description":"A Custom Jupyter Widget Library","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.js","dist/*.js","css/*.css"],"homepage":"https://github.com/paddymul/dcf","bugs":{"url":"https://github.com/paddymul/dcf/issues"},"license":"BSD-3-Clause","author":{"name":"Paddy Mullen","email":"paddy@paddymullen.com"},"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"https://github.com/paddymul/dcf"},"scripts":{"build":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension:dev","build:prod":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","build:nbextension":"webpack","clean":"yarn run clean:lib && yarn run clean:nbextension && yarn run clean:labextension","clean:lib":"rimraf lib","clean:labextension":"rimraf dcf/labextension","clean:nbextension":"rimraf dcf/nbextension/static/index.js","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","prepack":"yarn run build:lib","test":"jest","watch":"npm-run-all -p watch:*","watch:lib":"tsc -w","watch:nbextension":"webpack --watch --mode=development","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@jupyter-widgets/base":"^1.1.10 || ^2 || ^3 || ^4 || ^5 || ^6","paddy-react-edit-list":">=1.1.12","lodash":"^4.17.21","react-dom":"^18.0.0","react":"^18.0.0"},"devDependencies":{"@babel/core":"^7.5.0","@babel/preset-env":"^7.5.0","@jupyter-widgets/base-manager":"^1.0.2","@jupyterlab/builder":"^3.0.0","@lumino/application":"^1.6.0","@lumino/widgets":"^1.6.0","@types/jest":"^26.0.0","@types/react":"^18.0.0","@types/react-dom":"^18.0.0","@types/webpack-env":"^1.13.6","@typescript-eslint/eslint-plugin":"^3.6.0","@typescript-eslint/parser":"^3.6.0","acorn":"^7.2.0","css-loader":"^3.2.0","eslint":"^7.4.0","eslint-config-prettier":"^6.11.0","eslint-plugin-prettier":"^3.1.4","fs-extra":"^7.0.0","identity-obj-proxy":"^3.0.0","jest":"^26.0.0","mkdirp":"^0.5.1","npm-run-all":"^4.1.3","prettier":"^2.0.5","rimraf":"^2.6.2","source-map-loader":"^1.1.3","style-loader":"^1.0.0","ts-jest":"^26.0.0","ts-loader":"^8.0.0","typescript":"~4.1.3","webpack":"^5.61.0","webpack-cli":"^4.0.0"},"jupyterlab":{"extension":"lib/plugin","outputDir":"dcf/labextension/","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true},"react":false,"react-dom":false}}}');

/***/ })

}]);
//# sourceMappingURL=lib_index_js.4cd4476fba62a32f32e7.js.map