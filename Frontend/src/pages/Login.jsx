import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Container, Card, Form, Button, Alert } from 'react-bootstrap'
import api from '../services/api'
import { useAuth } from '../context/AuthContext'

export default function Login() {
  const [documentId, setDocumentId] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await api.post('/auth/login', {
        document_id: documentId,
        password: password,
      })
      login(response.data.access_token)
      navigate('/orders')
    } catch (err) {
      if (err.response && err.response.status === 401) {
        setError('Documento o contraseña incorrectos')
      } else {
        setError('No se pudo conectar con el servidor')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <Container className="d-flex justify-content-center align-items-center" style={{ minHeight: '100vh' }}>
      <Card style={{ width: '360px' }} className="p-4 shadow-sm">
        <Card.Body>
          <h4 className="mb-4 text-center">AridosCo</h4>

          {error && <Alert variant="danger">{error}</Alert>}

          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3">
              <Form.Label>Documento</Form.Label>
              <Form.Control
                type="text"
                value={documentId}
                onChange={(e) => setDocumentId(e.target.value)}
                required
              />
            </Form.Group>

            <Form.Group className="mb-4">
              <Form.Label>Contraseña</Form.Label>
              <Form.Control
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </Form.Group>

            <Button type="submit" variant="dark" className="w-100" disabled={loading}>
              {loading ? 'Ingresando...' : 'Ingresar'}
            </Button>
          </Form>
        </Card.Body>
      </Card>
    </Container>
  )
}