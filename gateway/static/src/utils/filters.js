export const privacyPhone = (phone) => {
  if (!phone) return '-'
  let privacyPhone = phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')
  return privacyPhone
}
export const dtime = (datetime, format = 'yyyy-MM-dd') => {
  if (!datetime) return '-'
  let t = new Date(datetime)
  let timeFormat = function (i) {
    return (i < 10 ? '0' : '') + i
  }
  return format.replace(/yyyy|MM|dd|hh|mm|ss/g, a => {
    switch (a) {
      case 'yyyy':
        return timeFormat(t.getFullYear())
      case 'MM':
        return timeFormat(t.getMonth() + 1)
      case 'dd':
        return timeFormat(t.getDate())
      case 'hh':
        return timeFormat(t.getHours())
      case 'mm':
        return timeFormat(t.getMinutes())
      case 'ss':
        return timeFormat(t.getSeconds())
    }
  })
}
export const toFixed = (val, num = 2) => {
  if (!val) return '—'
  return Number(val).toFixed(num)
}

export const errormsg = (error) => {
  const type = Object.prototype.toString
  const {message, description} = error
  let descArr = []
  let msg = message
  if (type.call(description) === '[object Object]') {
    Object.keys(description).forEach(key => {
      descArr.push(description[key])
    })
    msg = descArr[0][0]
  } else {
    msg = description || message
  }
  return msg
}
