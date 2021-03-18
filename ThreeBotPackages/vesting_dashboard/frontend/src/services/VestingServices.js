import Axios from 'axios';


const apiClient = Axios.create({
    baseURL: '/vesting_dashboard/api',
    withCredentials: true,
    headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
    }
})

export default {
    createAccount(address) {
        return apiClient.post('/account/create', { owner_address: address })
    },

}