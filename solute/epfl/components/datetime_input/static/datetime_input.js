epfl.DatetimeInput = function (cid, params) {
    epfl.FormInputBase.call(this, cid, params);
};

epfl.DatetimeInput.inherits_from(epfl.FormInputBase);

Object.defineProperty(epfl.DatetimeInput.prototype, 'form_element', {
    get: function () {
        return $("#" + this.cid + " input");
    }
});

epfl.DatetimeInput.prototype.DATE_FORMAT_LOCALE = "LL";
epfl.DatetimeInput.prototype.DATE_FORMAT_MONTH_YEAR = "MM[/]YYYY";
epfl.DatetimeInput.prototype.DATE_FORMAT_YEAR = "YYYY";
epfl.DatetimeInput.prototype.DATE_FORMAT_LOCALE_WITH_TIME = "LLL";
epfl.DatetimeInput.prototype.GERMAN_MONTHS = [
    "Januar",
    "Februar",
    "März",
    "April",
    "Mai",
    "Juni",
    "Juli",
    "August",
    "September",
    "Oktober",
    "November",
    "Dezember"];

epfl.DatetimeInput.prototype.to_utc = function(date){
    //Converts a string to a date, this is the fallback for all formats which momentjs cant handle
    var date_format = this.params["date_format"];
    if(date_format == epfl.DatetimeInput.prototype.DATE_FORMAT_LOCALE_WITH_TIME ){
        //example: 12. Juli 2015 00:00
        var parts = date.split(" ");
        var day = parts[0].slice(0,-1);
        var month = parts[1];
        month = this.GERMAN_MONTHS.indexOf(month);
        var year = parts[2];
        var time = parts[3].split(":");
        var hour = time[0];
        var min = time[1];
        date = new Date(year,month,day,hour,min,0,0);
    }else if(date_format == epfl.DatetimeInput.prototype.DATE_FORMAT_MONTH_YEAR){
        //example: 08/2015
        var parts = date.split("/");
        date = new Date(parts[1],parseInt(parts[0])-1,1,0,0,0,0);
    }else if(date_format == epfl.DatetimeInput.prototype.DATE_FORMAT_LOCALE){
        //example: 12. Juli 2015
        var parts = date.split(" ");
        var day = parts[0].slice(0,-1);
        var month = parts[1];
        month = this.GERMAN_MONTHS.indexOf(month);
        var year = parts[2];
        date = new Date(year,month,day,0,0,0,0);
    }

    return moment(date).locale("de").format();
};

epfl.DatetimeInput.prototype.custom_handle_change = function(event) {
    // custom handler needed, cause the value is not just $elm.val()
    var value = this.form_element.val();
    if(!value){
        value = null;
    } else {
        value = this.to_utc(value);
    }
    this.handle_change(event, value);
};

epfl.DatetimeInput.prototype.after_response = function (data) {
    epfl.FormInputBase.prototype.after_response.call(this, data);

    this.form_element.datetimepicker({
        locale: 'de',
        format: this.params["date_format"],
        icons: {
            time: 'fa fa-clock-o',
            date: 'fa fa-calendar',
            up: 'fa fa-angle-up',
            down: 'fa fa-angle-down',
            previous: 'fa fa-angle-left',
            next: 'fa fa-angle-right',
            today: 'fa fa-crosshairs',
            clear: 'fa fa-trash',
            close: 'fa fa-times'
        },
        useCurrent:false
    });

    this.form_element
        .blur(this.custom_handle_change.bind(this))
        .change(this.custom_handle_change.bind(this));

    if (this.params.value != null) {
        if (this.form_element.data("DateTimePicker")) {
            this.form_element.data("DateTimePicker").date(moment(this.params["value"]).locale("de"));
        }
    }
};
