const mongoose = require('mongoose');

const RideSchema = mongoose.Schema({
    name: {
        type: String,
        required: true
    },
    description: {
        type: String,
        required: true,
        trim: true
    },
    availableVehicles: {
        type: Array,
        required: true
    },
    category: {
        type: String,
        required: true
    },
    prebuilds: {
        type: Array,
        required: false
    }
}, 
// This is to keep my db clean at the sacrafice of version control.
{versionKey: false});

// ('referance name', 'Schema Name', 'DB Collection')
// I module exported to post via mongoose
module.exports = mongoose.model('ride', RideSchema, 'AvailableRides');