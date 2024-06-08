const cookieName = 'owm-ad'
const adParamInUrl = 'campaign_id'
const campaignIdKey = 'campaign_id'
const dateKey = 'date'

findAdCampaignInUrl()

function findAdCampaignInUrl () {
    var queryParams = window.location.search
    if (queryParams.length) {
      const params = queryParams.replace('?','').split('&')
      for (let i = 0; i < params.length; i += 1) {
        const [key, value] = params[i].split('=')
        if (key === adParamInUrl) {
          saveAdCampaignInCookies(value)
          break
        }
      }
    }
}

function saveAdCampaignInCookies (campaign) {
    const cookieContent = makeAdCookieContent(campaign)
    const cookieWithOptions = setOptions(cookieContent)
    document.cookie = cookieWithOptions
}

function makeAdCookieContent (campaign) {
    const openWebsiteDate = Math.round(new Date().getTime() / 1000)
    const cookieValue = encodeURIComponent(`${campaignIdKey}=${campaign}&${dateKey}=${openWebsiteDate}`)
    return `${cookieName}=${cookieValue}`
}

function setOptions (cookieContent) {
    const domainName = getDomainName()
    const expiryDate = expiryDateOneMonthFromNow()
    const options = { path: '/', expires: expiryDate, domain: domainName }
    const optionsArray = Object.keys(options)
    for (let i = 0; i < optionsArray.length; i += 1) {
      cookieContent += `;${optionsArray[i]}=${options[optionsArray[i]]}`
    }
    return cookieContent
}

function getDomainName () {
    const hostname = window.location.hostname
    const subDomain = hostname.split('.').splice(-2);
    return subDomain.join('.')
}

function expiryDateOneMonthFromNow () {
    const oneMonthInMs = 30 * 60 * 60 * 1000;
    const date = new Date();
    date.setTime(date.getTime() + oneMonthInMs)
    return date.toUTCString()
}
