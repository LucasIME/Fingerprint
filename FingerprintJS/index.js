"use strict";

class RingBuffer{
    constructor(size){
        this.buffer = new Array(size);
        this.len = size;
        this.currentIndex = 0;
        this.totalAdded = 0;
    }

    push(obj){
        this.buffer[this.currentIndex++] = obj;
        this.currentIndex %= this.len;
        this.totalAdded++;
    }

    getLast(n){
        if (n > this.len)
            throw new Error('Number should be smaller than Ring Buffer length');
        if(n > this.totalAdded)
            throw new Error("Number should not be greater than the number of items added to the Ring Buffer");
        var first = this.currentIndex;
        var last = 0;
        if(first >= 1){
            last = first - 1;
            if(last+1 >= n)
                return this.buffer.slice(last - n + 1, last+1);
            else
                return this.buffer.slice(first, first + n + 1 - (last+1)).concat(this.buffer.slice(0, last+1));
        }
        else{
            last = Math.min(this.len - 1, this.totalAdded-1);
            return this.buffer.slice(last - n + 1, last +1);
        }
    }
}

class Fingerprint{
    constructor(bufferSize){
        this.data = new RingBuffer(bufferSize);
    }

    processKeyDownEvent(evt){
        this.data.push([evt.key, "DOWN", (new Date()).getTime()]);
        console.log("DOWN", evt);
    }

    processKeyUpEvent(evt){
        this.data.push([evt.key, "UP", (new Date()).getTime()]);
        console.log("UP", evt);
    }

    get(length){
        var n = length || this.buffer.len;
        return this.buffer.getLast(n);
    }
}
