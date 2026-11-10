"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.default = handler;
const core_1 = require("@nestjs/core");
const platform_express_1 = require("@nestjs/platform-express");
const app_module_1 = require("../src/app.module");
const express_1 = __importDefault(require("express"));
let cachedServer;
async function bootstrapServer() {
    if (!cachedServer) {
        const expressApp = (0, express_1.default)();
        const adapter = new platform_express_1.ExpressAdapter(expressApp);
        const app = await core_1.NestFactory.create(app_module_1.AppModule, adapter);
        app.setGlobalPrefix('v1', {
            exclude: ['/', 'health'],
        });
        app.enableCors({
            origin: process.env.FRONTEND_URL || '*',
            credentials: true,
        });
        await app.init();
        cachedServer = expressApp;
    }
    return cachedServer;
}
async function handler(req, res) {
    try {
        const server = await bootstrapServer();
        return server(req, res);
    }
    catch (err) {
        console.error('Erro na inicialização do NestJS:', err);
        return res.status(500).json({ error: 'Internal Server Error' });
    }
}
//# sourceMappingURL=index.js.map