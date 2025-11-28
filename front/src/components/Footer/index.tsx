import styles from "./Footer.module.scss";

export default function Footer() {
    return (
        <footer className={styles.footer}>
            <div className={styles.footerContainer}>
                <div className={styles.copyright}>
                    ©&nbsp;2001&nbsp;— 2025&nbsp;ПАО «Банк ПСБ» Универсальная лицензия на&nbsp;осуществление банковских
                    операций со&nbsp;средствами в&nbsp;рублях и&nbsp;иностранной валюте (с&nbsp;правом привлечения
                    во&nbsp;вклады денежных средств физических лиц) и&nbsp;на&nbsp;осуществление банковских операций
                    с&nbsp;драгоценными металлами №&nbsp;3251, выдана Банком России 1&nbsp;апреля&nbsp;2025&nbsp;г.
                </div>
            </div>
        </footer>
    );
}
