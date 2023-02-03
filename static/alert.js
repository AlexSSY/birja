alert = {
    messageType: {
        "success": {
            image_html: `<svg fill="currentcolor" xmlns="http://www.w3.org/2000/svg" 
                                width="32px" height="32px" viewBox="0 0 52 52" enable-background="new 0 0 52 52" xml:space="preserve">
                        <path d="M26,2C12.7,2,2,12.7,2,26s10.7,24,24,24s24-10.7,24-24S39.3,2,26,2z M39.4,20L24.1,35.5
                            c-0.6,0.6-1.6,0.6-2.2,0L13.5,27c-0.6-0.6-0.6-1.6,0-2.2l2.2-2.2c0.6-0.6,1.6-0.6,2.2,0l4.4,4.5c0.4,0.4,1.1,0.4,1.5,0L35,15.5
                            c0.6-0.6,1.6-0.6,2.2,0l2.2,2.2C40.1,18.3,40.1,19.3,39.4,20z"/>
                        </svg>`,
            image_color: 'var(--success-text)',
            bg_color: 'var(--success-bg)',
            pre_title: 'Success:',
        },
        "warning": {
            image_html: `<svg width="32px" height="32px" viewBox="0 0 512 512" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                        <title>warning-filled</title>
                            <g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                                <g id="add" fill="currentcolor" transform="translate(32.000000, 42.666667)">
                                    <path d="M246.312928,5.62892705 C252.927596,9.40873724 258.409564,14.8907053 262.189374,21.5053731 L444.667042,340.84129 C456.358134,361.300701 449.250007,387.363834 428.790595,399.054926 C422.34376,402.738832 415.04715,404.676552 407.622001,404.676552 L42.6666667,404.676552 C19.1025173,404.676552 7.10542736e-15,385.574034 7.10542736e-15,362.009885 C7.10542736e-15,354.584736 1.93772021,347.288125 5.62162594,340.84129 L188.099293,21.5053731 C199.790385,1.04596203 225.853517,-6.06216498 246.312928,5.62892705 Z M224,272 C208.761905,272 197.333333,283.264 197.333333,298.282667 C197.333333,313.984 208.415584,325.248 224,325.248 C239.238095,325.248 250.666667,313.984 250.666667,298.624 C250.666667,283.264 239.238095,272 224,272 Z M245.333333,106.666667 L202.666667,106.666667 L202.666667,234.666667 L245.333333,234.666667 L245.333333,106.666667 Z" id="Combined-Shape">
                                    </path>
                                </g>
                            </g>
                        </svg>`,
            image_color: 'var(--warning-text)',
            bg_color: 'var(--warning-bg)',
            pre_title: 'Warning:',
        },
        "error": {
            image_html: `<svg width="32px" height="32px" viewBox="0 0 24 24" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                            <!-- Uploaded to: SVG Repo, www.svgrepo.com, Generator: SVG Repo Mixer Tools -->
                            <title>ic_fluent_error_circle_24_filled</title>
                            <desc>Created with Sketch.</desc>
                            <g id="🔍-System-Icons" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                                <g id="ic_fluent_error_circle_24_filled" fill="currentcolor" fill-rule="nonzero">
                                    <path d="M12,2 C17.523,2 22,6.478 22,12 C22,17.522 17.523,22 12,22 C6.477,22 2,17.522 2,12 C2,6.478 6.477,2 12,2 Z M12.0018002,15.0037242 C11.450254,15.0037242 11.0031376,15.4508407 11.0031376,16.0023869 C11.0031376,16.553933 11.450254,17.0010495 12.0018002,17.0010495 C12.5533463,17.0010495 13.0004628,16.553933 13.0004628,16.0023869 C13.0004628,15.4508407 12.5533463,15.0037242 12.0018002,15.0037242 Z M11.99964,7 C11.4868042,7.00018474 11.0642719,7.38637706 11.0066858,7.8837365 L11,8.00036004 L11.0018003,13.0012393 L11.00857,13.117858 C11.0665141,13.6151758 11.4893244,14.0010638 12.0021602,14.0008793 C12.514996,14.0006946 12.9375283,13.6145023 12.9951144,13.1171428 L13.0018002,13.0005193 L13,7.99964009 L12.9932303,7.8830214 C12.9352861,7.38570354 12.5124758,6.99981552 11.99964,7 Z" id="🎨-Color">
                                    </path>
                                </g>
                            </g>
                        </svg>`,
            image_color: 'var(--error-text)',
            bg_color: 'var(--error-bg)',
            pre_title: 'Error:',
        },
        "info": {
            image_html: `<svg width="32px" height="32px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path fill-rule="evenodd" clip-rule="evenodd" d="M1 12C1 5.92487 5.92487 1 12 1C18.0751 1 23 5.92487 23 12C23 18.0751 18.0751 23 12 23C5.92487 23 1 18.0751 1 12ZM10.25 11C10.25 10.4477 10.6977 10 11.25 10H12.75C13.3023 10 13.75 10.4477 13.75 11V18C13.75 18.5523 13.3023 19 12.75 19H11.25C10.6977 19 10.25 18.5523 10.25 18V11ZM14 7C14 5.89543 13.1046 5 12 5C10.8954 5 10 5.89543 10 7C10 8.10457 10.8954 9 12 9C13.1046 9 14 8.10457 14 7Z" fill="currentcolor"/>
                        </svg>`,
            image_color: 'var(--info-text)',
            bg_color: 'var(--info-bg)',
            pre_title: 'Info:',
        }
    },
    getTemplate(msg_type, message, title) {
        return ` <div class="alert-bg"></div>
                <div class="alert" style="color: ${msg_type.bg_color};">
                    <div class="alert__image" style="color: ${msg_type.image_color};">
                        ${msg_type.image_html}
                    </div>
                    <div class="alert__body">
                        <div class="alert__header">
                            <p class="alert__title" style="color: ${msg_type.image_color};">
                                <span style="font-weight: 700;">${msg_type.pre_title}</span> 
                                ${title}
                            </p>
                        </div>
                        <div class="alert__message">
                            <p class="alert__text" style="color: ${msg_type.image_color};">
                                ${message}
                            </p>
                        </div>
                    </div>
                    <button class="alert__button" style="color: ${msg_type.image_color};">
                        <svg width="32px" height="32px" viewBox="0 0 1024 1024" class="icon" xmlns="http://www.w3.org/2000/svg">
                            <path fill="currentcolor" d="M195.2 195.2a64 64 0 0190.496 0L512 421.504 738.304 195.2a64 64 0 0190.496 90.496L602.496 512 828.8 738.304a64 64 0 01-90.496 90.496L512 602.496 285.696 828.8a64 64 0 01-90.496-90.496L421.504 512 195.2 285.696a64 64 0 010-90.496z"/>
                        </svg>
                    </button>
                </div>`;
    },
    show(msg_type, message, title) {
        this.rootElement = $(this.getTemplate(msg_type, message, title));
        $('body').append(this.rootElement);

        $(this.rootElement).find('button').on('click', () => {
            this.destroy();
        });
    },
    destroy() {
        if (this.rootElement)
            this.rootElement.remove();
    }
}

alert_yesno = {
    getTemplate(msg_type, message, title) {
        return ` <div class="alert-bg"></div>
                <div class="alert" style="color: ${msg_type.bg_color};">
                    <div class="alert__image" style="color: ${msg_type.image_color};">
                        ${msg_type.image_html}
                    </div>
                    <div class="alert__body">
                        <div class="alert__header">
                            <p class="alert__title" style="color: ${msg_type.image_color};">
                                <span style="font-weight: 700;">${msg_type.pre_title}</span> 
                                ${title}
                            </p>
                        </div>
                        <div class="alert__message">
                            <p class="alert__text" style="color: ${msg_type.image_color};">
                                ${message}
                            </p>
                        </div>
                    </div>
                    <button class="alert__button" style="color: ${msg_type.image_color};">
                        <svg width="32px" height="32px" viewBox="0 0 1024 1024" class="icon" xmlns="http://www.w3.org/2000/svg">
                            <path fill="currentcolor" d="M195.2 195.2a64 64 0 0190.496 0L512 421.504 738.304 195.2a64 64 0 0190.496 90.496L602.496 512 828.8 738.304a64 64 0 01-90.496 90.496L512 602.496 285.696 828.8a64 64 0 01-90.496-90.496L421.504 512 195.2 285.696a64 64 0 010-90.496z"/>
                        </svg>
                    </button>
                </div>`;
    },
    show(msg_type, message, title) {
        this.rootElement = $(this.getTemplate(msg_type, message, title));
        $('body').append(this.rootElement);

        $(this.rootElement).find('button').on('click', () => {
            this.destroy();
        });
    },
    destroy() {
        if (this.rootElement)
            this.rootElement.remove();
    }
}