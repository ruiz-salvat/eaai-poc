<template>
    <div>
        hola
            <!-- <input type="text" name="username" placeholder="username">
            <button @click="submit()">Login / Signup</button> -->
            <hr>
            <form :action="homeUrl" method="post">
                <input type="text" name="username" placeholder="username">
                <button type="submit">Login / Signup</button>
            </form>

            <hr>

            <form :action="createClientUrl" method="post">
            <label>
                <span>Client Name</span>
                <input type="text" name="client_name">
            </label>
            <label>
                <span>Client URI</span>
                <input type="url" name="client_uri">
            </label>
            <label>
                <span>Allowed Scope</span>
                <input type="text" name="scope">
            </label>
            <label>
                <span>Redirect URIs</span>
                <textarea name="redirect_uri" cols="30" rows="10"></textarea>
            </label>
            <label>
                <span>Allowed Grant Types</span>
                <textarea name="grant_type" cols="30" rows="10"></textarea>
            </label>
            <label>
                <span>Allowed Response Types</span>
                <textarea name="response_type" cols="30" rows="10"></textarea>
            </label>
            <label>
                <span>Token Endpoint Auth Method</span>
                <select name="token_endpoint_auth_method">
                <option value="client_secret_basic">client_secret_basic</option>
                <option value="client_secret_post">client_secret_post</option>
                <option value="none">none</option>
                </select>
            </label>
            <button>Submit</button>
            </form>
    </div>
</template>

<script>
export default {
    created() {
        fetch(`${import.meta.env.VITE_API_URL}user`, {
              method: 'GET',
              headers: {
                'Content-Type': 'application/json',
                // 'Authorization': `Bearer ${api_key}`
              },
            //   body: JSON.stringify(jsonData)
            }).then((response) => response.json())
            .then((response) => {
                console.log('response', response)
            })
    },
    methods: {
        objectToFormData(obj) {
        const formData = new FormData();
        for (const [key, value] of Object.entries(obj)) {
            formData.append(key, value);
        }
        return formData;
        },
        submit() {
            let data = {username: 'ekiki'}
            
            const formData = this.objectToFormData(data)

            fetch(`${import.meta.env.VITE_API_URL}home`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: formData
            }).then((response) => response.json())
            .then((response) => {
                console.log('response', response)
            })
        }
    },
    computed: {
        homeUrl() {
            return `${import.meta.env.VITE_API_URL}home`
        },
        createClientUrl() {
            return `${import.meta.env.VITE_API_URL}create_client`
        }
    },
}
</script>