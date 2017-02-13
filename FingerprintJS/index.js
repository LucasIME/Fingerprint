"use strict";

class Fingerprint{
    constructor(){
        this.data = [];
    }

    processKeyDownEvent(evt){
        this.data.push([evt.key, "DOWN", (new Date()).getTime()]);
        console.log("DOWN", evt);
    }

    processKeyUpEvent(evt){
        this.data.push([evt.key, "UP", (new Date()).getTime()]);
        console.log("UP", evt);
    }
}
