"use strict";

class RingBuffer<T>{
    
    buffer : Array<T>;
    len : number;
    currentIndex : number;
    totalAdded : number;

    constructor(size: number){
        this.buffer = new Array(size);
        this.len = size;
        this.currentIndex = 0;
        this.totalAdded = 0;
    }

    push(obj : T) : void{
        this.buffer[this.currentIndex++] = obj;
        this.currentIndex %= this.len;
        this.totalAdded++;
    }

    getLast(n : number) : Array<T>{
        if (n > this.len)
            throw new Error('Number should be smaller than Ring Buffer length');
        if(n > this.totalAdded)
            throw new Error("Number should not be greater than the number of items added to the Ring Buffer");
        let first = this.currentIndex;
        let last = 0;
        if(first >= 1){
            last = first - 1;
            if(last+1 >= n)
                return this.buffer.slice(last - n + 1, last+1);
            else
                return this.buffer.slice(this.len - n + last + 1, this.len).concat(this.buffer.slice(0, last+1));
        }
        else{
            last = Math.min(this.len - 1, this.totalAdded-1);
            return this.buffer.slice(last - n + 1, last +1);
        }
    }
}

export class Keystroke {
    key : string;
    direction : string;
    timestamp : number;

    constructor(key: string, direction: string, timestamp: number ){
        this.key = key;
        this.direction = direction;
        this.timestamp = timestamp;
    }
}

export class Fingerprint{
    buffer : RingBuffer<Keystroke>;

    constructor(bufferSize : number){
        this.buffer = new RingBuffer<any>(bufferSize);
    }

    processKeyDownEvent(evt) : void{
        this.buffer.push(new Keystroke(evt.key, "DOWN", evt.timeStamp));
        console.log("DOWN", evt);
    }

    processKeyUpEvent(evt) : void{
        this.buffer.push(new Keystroke(evt.key, "UP", evt.timeStamp));
        console.log("UP", evt);
    }

    get(length : number) : Array<Keystroke> {
        let n = length || Math.min(this.buffer.len, this.buffer.totalAdded);
        return this.buffer.getLast(n);
    }
}

