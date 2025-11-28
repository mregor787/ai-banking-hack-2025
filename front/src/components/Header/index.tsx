import LogoPSB from "@/components/LogoPSB";
import LogoMAI from "@/components/LogoMAI";

import styles from "./Header.module.scss";

export default function Header() {
    return (
        <header className={styles.header}>
            <div className={styles.headerContainer}>
                <LogoPSB />
                <h1 className={styles.title}>ИИ-Ассистент</h1>
                <LogoMAI className={styles.logo} />
            </div>
        </header>
    );
}
