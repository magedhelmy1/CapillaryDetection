import React from 'react';
import {Nav, Navbar} from 'react-bootstrap';

const Navigation = () => {
    return (
        <Navbar bg="dark" variant="dark" className="mb-3">
            <Navbar.Brand href="#home">CapillaryWeb Demo</Navbar.Brand>
            <Nav className="mr-auto">
                <Nav.Link href="/">Home</Nav.Link>
            </Nav>
        </Navbar>
    );
}

export default Navigation;
