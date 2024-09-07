<template>
    <div>

        <h1>Login</h1>

        <div>
            <label>
                <span>Username</span>
                <input type="text" name="username" v-model="username">
            </label>
            <button @click="getUserId()">Submit</button>
        </div>

        <div>User id: {{ userId }}</div>

        <hr>

        <div>
            <label>
                <span>Create Client</span>
                <!-- <input type="text" name="username"> -->
            </label>
            <div>
                <button @click="createClient()">Submit</button>
            </div>

            <div>client id: {{ this.clientId }}</div>
            <div>client secret: {{ this.clientSecret }}</div>
        </div>

        <hr>

        <div>
            <label>
                <span>Authorize</span>
                <!-- <input type="text" name="username"> -->
            </label>
            <div>
                <button @click="authorize()">Submit</button>
            </div>

            <div>authorization code: {{ this.authorizationCode}}</div>
        </div>

        <hr>

        <div>
            <label>
                <span>Issue token</span>
                <!-- <input type="text" name="username"> -->
            </label>
            <div>
                <button @click="issueToken()">Submit</button>
            </div>
        </div>

    </div>
</template>

<script>
export default {
    data() {
        return {
            userId: null,
            username: null,
            clientId: null,
            clientSecret: null,
            authorizationCode: null
        }
    },
    created() {
        // fetch(`${import.meta.env.VITE_API_URL}user`, {
        //       method: 'GET',
        //       headers: {
        //         'Content-Type': 'application/json',
        //         // 'Authorization': `Bearer ${api_key}`
        //       },
        //     //   body: JSON.stringify(jsonData)
        //     }).then((response) => response.json())
        //     .then((response) => {
        //         console.log('response', response)
        //     })
    },
    methods: {
        objectToFormData(obj) {
            const formData = new FormData()
            for (const [key, value] of Object.entries(obj)) {
                formData.append(key, value)
            }
            return formData
        },
        getUserId() {
            let data = {username: this.username}
            
            const formData = this.objectToFormData(data)

            console.log('form data', formData)

            fetch(`${import.meta.env.VITE_API_URL}home`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
              },
              body: new URLSearchParams(formData).toString()
            }).then((response) => response.json())
            .then((response) => {
                this.userId = response.user_id
            })
        },
        createClient() {
            let data = { // TODO: move some values to backend
                client_name: this.username,
                client_uri: 'http://127.0.0.1:5173/plan',
                grant_types: 'authorization_code',
                redirect_uris: 'http://127.0.0.1:5173/plan',
                response_types: 'code',
                scope: 'profile',
                token_endpoint_auth_method: 'client_secret_basic'
            }
            
            const formData = this.objectToFormData(data)

            console.log('form data', formData)

            fetch(`${import.meta.env.VITE_API_URL}create-client`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Id': `${this.userId}`
              },
              body: new URLSearchParams(formData).toString()
            }).then((response) => response.json())
            .then((response) => {
                this.clientId = response.client_id
                this.clientSecret = response.client_secret
            })
        },
        authorize() {
            let data = {
                confirm: true,
                username: this.username
            }
            
            const formData = this.objectToFormData(data)

            fetch(`${import.meta.env.VITE_API_URL}authorize?response_type=code&client_id=${this.clientId}&scope=profile`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Id': `${this.userId}`
              },
              body: new URLSearchParams(formData).toString()
            }).then((response) => response.json()).then((data) => {
                this.authorizationCode = data.authorization_code
            })
        },
        issueToken() {
            let data = {
                code: this.authorizationCode,
                scope: 'profile',
                grant_type: 'authorization_code'
            }
            
            const formData = this.objectToFormData(data)

            const encodedCredentials = btoa(`${this.clientId}:${this.clientSecret}`)

            const authorizationHeader = `Basic ${encodedCredentials}`

            fetch(`${import.meta.env.VITE_API_URL}issue-token`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Id': `${this.userId}`,
                'Authorization': authorizationHeader
              },
              body: new URLSearchParams(formData).toString()
            }).then((response) => {
                console.log('status', response.status)
                console.log('headers', response.headers)
                return response.json()
            }).then((data) => {
                console.log('token successfully created', data)
            })
        }
    },
    computed: {
        homeUrl() {
            return `${import.meta.env.VITE_API_URL}home?next=http://localhost:5173/plan`
        },
        createClientUrl() {
            return `${import.meta.env.VITE_API_URL}create_client`
        }
    },
}
</script>