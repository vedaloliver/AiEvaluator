import { NextResponse } from 'next/server';
import axios from 'axios';

const EVALUATOR_SERVICE_URL =
  process.env.EVALUATOR_SERVICE_URL || 'http://localhost:3001';

export async function GET() {
  try {
    const response = await axios.get(
      `${EVALUATOR_SERVICE_URL}/api/v1/scenarios`,
      {
        timeout: 10000,
      }
    );

    return NextResponse.json(response.data);
  } catch (error) {
    console.error('Failed to fetch scenarios:', error);
    return NextResponse.json(
      {
        error: {
          message: 'Failed to fetch scenarios from evaluator service',
          statusCode: 500,
        },
      },
      { status: 500 }
    );
  }
}
