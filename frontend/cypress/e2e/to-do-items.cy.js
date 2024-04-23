describe('Test todo item', () => {
    // define variables that we need on multiple occasions
    let uid // user id
    let name // name of the user (firstName + ' ' + lastName)
    let email // email of the user
    let taskId // task created for test

    before(function () {
        // create a fabricated user from a fixture
        cy.fixture('user.json')
        .then((user) => {
            cy.request({
            method: 'POST',
            url: 'http://localhost:5000/users/create',
            form: true,
            body: user
            }).then((response) => {
            uid = response.body._id.$oid
            name = user.firstName + ' ' + user.lastName
            email = user.email
            })
        })

        //Add a fabricated task to the user from a fixture
        cy.fixture('task.json')
        .then((task) => {
            cy.request({
                method: 'POST',
                form: true,
                url: 'http://localhost:5000/tasks/create',
                body: {
                    ...task,
                    "userid": uid
                }
            })
        }).then((response) => {
            taskId = response.body[0]._id.$oid
        })
    })

    beforeEach(function () {
        // enter the main page and sign in
        cy.visit('http://localhost:3000')

        cy.contains('div', 'Email Address')
        .find('input[type=text]')
        .type(email)

        cy.get('form')
        .submit()

        cy.contains('div', 'Testing Task').click()
    })

    it('Todo item is empty', () => {
        cy.get('.popup-inner')
        .find('form.inline-form')
        .find('input[type=submit]')
        .should('be.disabled')
    })

    it('Todo item can be toggled', () => {
        cy.get('.popup-inner')
        .find('ul.todo-list')
        .first()
        .find('.checker').as('checker')

        cy.get('@checker')
        .click()

        cy.get('@checker')
        .should('have.class', 'checked')

        cy.get('@checker')
        .click()

        cy.get('@checker')
        .should('have.class', 'unchecked')
    })

    it('Adding todo item', () => {
        // Add a new todo item with a valid description
        cy.get('.popup-inner')
        .find('form.inline-form')
        .find('input[type=text]')
        .type('Another todo item')

        cy.get('.popup-inner')
        .find('form.inline-form')
        .find('input[type=submit]')
        .click()

        cy.get('.popup-inner')
        .find('ul.todo-list')
        .should('contain', 'Another todo item')
    })

    it('Removing todo item', () => {
        cy.get('.popup-inner')
        .find('ul.todo-list')
        .find('span.remover')
        .first()
        .click()

        cy.get('.popup-inner')
        .find('ul.todo-list')
        .first()
        .should('not.contain.text', 'First test item of todo list')
    })

    after(function () {
        // clean up by deleting the user from the database
        cy.request({
            method: 'DELETE',
            url: `http://localhost:5000/users/${uid}`
        }).then((response) => {
            cy.log(response.body)
        })
    })
})