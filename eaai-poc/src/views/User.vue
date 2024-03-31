<template>
    <div>
        hola
            <input type="text" name="username" placeholder="username">
            <button @click="submit()">Login / Signup</button>
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
    }
}
</script>