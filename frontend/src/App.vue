<script lang="ts">
import {defineComponent} from 'vue';

export default defineComponent({
    methods: {
        calculate: function () {
            console.log(this.data)
            let host = import.meta.env.VITE_HOST
            fetch(host + '/calc', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.data)
            }).then((response) => response.json()).then(this.process_calculate_answer)
        },
        process_calculate_answer: function (data) {
            this.errors = {}
            this.results = []

            if (data.state == 'error') {
                console.log(data)
                data.errors.forEach(error => {
                    this.errors[error.code] = error.text
                })

                console.log(this.errors)
            } else {
                this.results = data.results
            }
        },
        init: function (data) {
            this.fields = data['fields']

            this.fields.forEach(field => {
                if (field.limits) {
                    this.fields_limits[field.code] = {}
                    field.limits.forEach((limit) => {
                        this.fields_limits[field.code][limit.type] = limit.value
                    })
                }

                if (field.type == 'radio') {
                    this.data[field.code] = field.options[0].value
                }
            })

            this.title = data['title']
            this.info = data['info']
        }
    },
    data() {
        return {
            fields: [],
            title: "",
            info: "",
            fields_limits: {},
            data: {},
            results: [],
            errors: {}
        }
    },
    mounted() {
        let host = import.meta.env.VITE_HOST

        fetch(host + '/calc')
            .then((response) => response.json())
            .then(this.init);
    }
})

</script>

<template>
    <div class="container mt-3">
        <div class="is-centered">
            <div class="column is-full">
                <div class="box main-block">

                    <h1 class="title is-4">{{ title }}</h1>

                    <div class="field" v-for="field in fields">

                        <label class="label">{{ field.title }}</label>


                        <div class="field is-expanded">
                            <div class="field has-addons">

                                <div class="control is-expanded">
                                    <input :class="{'is-danger': errors[field.code]}" v-if="field.type === 'string'"
                                           class="input" type="text"
                                           v-model="data[field.code]">
                                    <input :class="{'is-danger': errors[field.code]}" v-if="field.type === 'int'"
                                           class="input" type="number" step="1"
                                           v-model="data[field.code]" :min="fields_limits[field.code].min"
                                           :max="fields_limits[field.code].max">
                                    <input :class="{'is-danger': errors[field.code]}" v-if="field.type === 'float'"
                                           class="input" type="number" step="0.01"
                                           v-model="data[field.code]" :min="fields_limits[field.code].min"
                                           :max="fields_limits[field.code].max">

                                    <div :class="{'is-danger': errors[field.code]}" class="select"
                                         v-if="field.type === 'radio'">
                                        <select v-model="data[field.code]">
                                            <option v-for="option in field.options" :value="option.value">{{
                                                    option.title
                                                }}
                                            </option>
                                        </select>
                                    </div>
                                </div>

                                <p class="control" v-if="['int', 'float', 'string'].includes(field.type)">
                                    <a class="button is-static">
                                        {{ field.unit }}
                                    </a>
                                </p>
                            </div>
                        </div>


                        <p class="help"><span v-if="field.description">{{
                                field.description
                            }} </span></p>

                        <p class="help is-danger" v-if="errors[field.code]">{{ errors[field.code] }}</p>
                    </div>

                    <div class="field is-grouped">
                        <div class="control">
                            <button @click="calculate" class="button is-link">Отправить</button>
                        </div>
                    </div>

                    <article class="message is-info" v-for="result in results">
                        <div class="message-header">
                            <p>{{ result.title }}</p>
                        </div>
                        <div class="message-body">
                            {{ result.value }} {{ result.unit }}
                        </div>
                    </article>

                    <div class="content" v-for="block in info">

                        <h6 class="subtitle is-5">{{ block['title'] }}</h6>

                        <p v-for="paragraph in block['text'].split('\n')">{{ paragraph }}</p>

                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.main-block {
    max-width: 800px;
    margin: 0 auto;
}
</style>
