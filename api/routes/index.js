const express = require('express');
const router = express.Router();
const AvailableRide = require('../models/AvailableRides');

// Root route
router.get('/', (req, res) => {
    res.render('index', {title: 'RCT Rides From'});
});


// Posts data into the DB
// Only using as a tool so I don't have to write the DB queries
router.post('/', (req, res) => {

    // Lazy way of getting my stuff into array
    const convertStringToArray = (formElement) => {
        const inputString = formElement;
        const resultArray = inputString.split(',');
        return resultArray;
    }

    // Making Object to send to Mongo
    const newRide = new AvailableRide({
        name: req.body.name,
        description: req.body.description,
        availableVehicles: convertStringToArray(req.body.availableVehicles),
        category: req.body.category,
        prebuilds: convertStringToArray(req.body.prebuilds)
    });

    // Saving Object into Collection
    newRide.save()
    .then(result => {
        console.log(result);
    })
    .catch(error => {
        console.error(error);
    });

    // Rerenders the form page
    res.render('index', {title: 'Form posted'});
})

module.exports = router;