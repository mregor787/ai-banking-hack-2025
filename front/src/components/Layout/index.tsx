import { ReactNode } from "react";

import Header from "@/components/Header";
import Footer from "@/components/Footer";

import styles from "./Layout.module.scss";

interface LayoutProps {
    children: ReactNode;
}

export default function Layout({ children }: LayoutProps) {
    return (
        <div className={styles.content}>
            <Header />
            <main className={styles.mainConteiner}>{children}</main>
            <Footer />
        </div>
    );
}
