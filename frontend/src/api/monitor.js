import axios from 'axios';

// 获取主机列表
export function getHosts() {
    return axios.get('/monitor/hosts');
}

// 获取监控指标
// params: { host, measurement, fields, start, stop, window }
export function getMetrics(params) {
    return axios.get('/monitor/metrics', { params });
}